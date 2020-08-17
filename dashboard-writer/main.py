import mdf_iter, canedge_browser, can_decoder
from utils import setup_fs, setup_fs_s3, write_influx, load_last_run, set_last_run
import inputs

# function for loading raw CAN data from S3, DBC converting it and writing it to InfluxDB
def process_data_and_write():

    # initialize DBC converter and file loader
    db = can_decoder.load_dbc(inputs.dbc_path)
    df_decoder = can_decoder.DataFrameDecoder(db)

    # List log files from your local disk or S3 server from the loaded start date
    start = load_last_run("last_run.txt")

    # load data from local disk or from S3
    if inputs.use_s3:
        fs = setup_fs_s3()
    else:
        fs = setup_fs()

    if inputs.use_dynamic:
        print("Set the execution time for use in the next run")
        set_last_run("last_run.txt")

    log_files = canedge_browser.get_log_files(
        fs, inputs.devices, start_date=start, stop_date=inputs.stop
    )
    print(f"Found a total of {len(log_files)} log files")

    for log_file in log_files:
        # open log file, get device_id and extract dataframe with raw CAN data
        with fs.open(log_file, "rb") as handle:
            mdf_file = mdf_iter.MdfFile(handle)
            device_id = mdf_file.get_metadata()[
                "HDComment.Device Information.serial number"
            ]["value_raw"]
            df_raw = mdf_file.get_data_frame()

        # DBC convert the raw CAN dataframe
        df_phys = df_decoder.decode_frame(df_raw)
        if df_phys.empty:
            continue

        print(f"\nExtracted a total of {len(df_phys)} decoded messages")

        # group the data to enable a signal-by-signal loop
        df_phys_grouped = df_phys.groupby("Signal")["Physical Value"]

        # for each signal in your list, resample the data and write to InfluxDB
        for signal, group in df_phys_grouped:
            if signal in inputs.signals or len(inputs.signals) == 0:
                df_phys_signal = group.to_frame().rename(
                    columns={"Physical Value": signal}
                )

                if inputs.res != "":
                    df_phys_signal = df_phys_signal.resample(inputs.res).pad().dropna()

                print(df_phys_signal)
                write_influx(device_id, df_phys_signal)

    return


# execute the script
if __name__ == "__main__":

    process_data_and_write()
    pass
