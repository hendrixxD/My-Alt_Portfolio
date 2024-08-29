def _to_parquet(data):
    # TODO: 
    pass


def _to_csv(data):
    # TODO
    pass


def _to_avro(data):
    # TODO
    pass


def export_factory(data, file_format):
    #TODO
    factory = {
        "csv": _to_csv,
        "parquet": _to_parquet,
        "avro": _to_avro
    }

    return factory(file_format)


file_format_a = "csv"

fileFormat_b = "avro"

data_a = "the data"

data_b = "the second data!!"

export_factory(file_format=file_format_a)(data_a)
