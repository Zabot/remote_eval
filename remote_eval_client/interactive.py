import client

previous_results = {}

while True:
    print(">>>", end='')
    code = input()

    if code.startswith('?'):
        print(eval(code[1:], None, previous_results))

    else:
        result = client.execute(code)
        if (result):
            result_key = "r{}".format(len(previous_results))
            print("({}) {}".format(result_key, result))
            previous_results[result_key] = result

