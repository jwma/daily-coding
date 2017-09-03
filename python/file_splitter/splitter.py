import os


class Splitter(object):
    def __write_new_file(self, file_idx=0, content='', file_ext='', **kwargs):
        prefix = kwargs.get('prefix', '')
        try:
            with open('./result/{0}{1}{2}'.format(prefix, file_idx, file_ext), 'w') as new_file:
                new_file.writelines(content)
            return True
        except IOError as e:
            print(e)
            return False

    def split_file(self, filename='', count=500, clean_line_handler=None, mk_content_handler=None, **kwargs):
        counter = 1
        lines = []
        file_idx = 0
        file_ext = os.path.splitext(filename)[1]
        has_clean_line_handler = callable(clean_line_handler)
        has_mk_content_handler = callable(mk_content_handler)

        try:
            with open(filename, 'r') as target_file:
                for line in target_file:
                    lines.append(clean_line_handler(line) if has_clean_line_handler else line)

                    if counter >= count:
                        new_content = mk_content_handler(lines) if has_mk_content_handler else ''.join(lines)
                        self.__write_new_file(file_idx, new_content, file_ext, **kwargs)

                        lines = []
                        counter = 1
                        file_idx += 1
                        continue

                    counter += 1

                if len(lines) > 0:
                    new_content = mk_content_handler(lines) if has_mk_content_handler else ''.join(lines)
                    self.__write_new_file(file_idx, new_content, file_ext, **kwargs)

            return True
        except IOError as e:
            print(e)
            return False


if __name__ == '__main__':
    def my_clean_line_handler(line=''):
        return line.replace('"', '').rstrip()


    def my_mk_content_handler(lines=None):
        return ','.join(lines)


    splitter = Splitter()

    """
    分割test_data.txt文件，
    每个文件包含2行，
    生成的分块文件前缀为t1
    """
    print(splitter.split_file('./test_data.txt', 2, prefix='t1_'))

    """
    分割test_data.txt文件，每个文件包含4行，
    每行内容经过my_clean_line_handler处理，
    每次写入分块文件前内容经过my_mk_content_handler处理
    生成的分块文件前缀为t2
    """
    print(splitter.split_file('./test_data.txt', 4, my_clean_line_handler, my_mk_content_handler, prefix='t2_'))
