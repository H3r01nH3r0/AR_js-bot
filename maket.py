class Maket_to_HTML:

    def __init__(self, maket_file):
        self.maket = maket_file

    def object(self, link, user_id):
        with open(self.maket, 'r') as maket:
            with open(f'privat-links/{user_id}.html', 'w+') as file:
                for line in maket.readlines():
                    if 'gltf' in line:
                        line = line.format(link)
                        file.write(line)
                    else:
                        file.write(line)

    def text(self, link, user_id):
        with open(self.maket, 'r') as maket:
            with open(f'privat-links/{user_id}.html', 'w+') as file:
                for line in maket.readlines():
                    if 'text' in line:
                        line = line.format(link)
                        file.write(line)
                    else:
                        file.write(line)


    def picture(self, link, user_id):
        with open(self.maket, 'r') as maket:
            with open(f'privat-links/{user_id}.html', 'w+') as file:
                for line in maket.readlines():
                    if '<a-image' in line:
                        line = line.format(link)
                        file.write(line)
                    else:
                        file.write(line)


