import time


def new_test(name = ""):
    return (time.monotonic(), name)
  
def test_end(test_data):
    elapsed_time = time.monotonic() - test_data[0]
    if (elapsed_time > 0.1):
        print(f"{test_data[1]} test execution time: {elapsed_time}")
