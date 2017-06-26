from rfid_mfrc522 import RFIDReader

input_threads = []


def start_all_input_threads():
    rfid_reader = RFIDReader()
    rfid_reader.start()
    input_threads.append(rfid_reader)
    return input_threads


def stop_all_input_threads():
    for thread in input_threads:
        thread.shutdown()
    return input_threads


def is_all_input_threads_alive():
    for thread in input_threads:
        if not thread.is_alive():
            return False
    return True
