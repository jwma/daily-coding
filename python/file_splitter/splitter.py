def write_new_file(file_idx=0, content=''):
    new_file = open('./result/{0}.txt'.format(file_idx), 'w')
    new_file.writelines(content)
    new_file.close()


def split_file(filename='', count=500, clean_line_handler=None, mk_content_handler=None):
    file_idx = 0
    counter = 1
    lines = []

    has_clean_line_handler = callable(clean_line_handler)
    has_mk_content_handler = callable(mk_content_handler)

    try:
        with open(filename, 'r') as target_file:
            for line in target_file:
                if has_clean_line_handler:
                    lines.append(clean_line_handler(line))
                else:
                    lines.append(line)

                if counter > count:
                    if has_mk_content_handler:
                        write_new_file(file_idx, mk_content_handler(lines))
                    else:
                        write_new_file(file_idx, ''.join(lines))

                    lines = []
                    counter = 1
                    file_idx += 1

                    continue

                counter += 1

            if len(lines) > 0:
                if has_mk_content_handler:
                    write_new_file(file_idx, mk_content_handler(lines))
                else:
                    write_new_file(file_idx, ''.join(lines))

            return True
    except IOError as e:
        print(e)
        return False


if __name__ == '__main__':
    def my_clean_line_handler(line=''):
        return line.replace('"', '').rstrip()


    def my_mk_content_handler(lines=None):
        return ','.join(lines)


    print(split_file('./test_data.txt', 3, my_clean_line_handler, my_mk_content_handler))
