from datetime import datetime
from pyquery import PyQuery as pquery

import urllib3
urllib3.disable_warnings()



def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def main():
    active = 'https://webbtelescope.org/contents/media/images/2022/028/01G77Q8BTTSEB7ZSB2ZEY49HSQ'

    print(f'{timestamp()} Starting...')

    count=0
    previous = ''
    while (active):
        py = pquery(active, verify=False)

        span = py.find("span")
        spans = [i.text() for i in span.items()]

        try:
            next_idx = spans.index("Next")
            next = 'https://webbtelescope.org' + [i.attr("href") for i in span.eq(next_idx).parent().items()][0]
        except ValueError:
            if count == 247:
                pass
            else:
                print(previous)
                print(active)
                print(count)
                print(timestamp())
                raise

        downloads = py.find("div.media-library-links-list").find('a')

        imgs_text = [i.text() for i in downloads.items()]
        imgs_links = [i.attr('href') for i in downloads.items()]

        full_res_str = [i for i in imgs_text if i.startswith('Full') and 'TIF' not in i] # Full Res first
        if not full_res_str:
            full_res_str = [i for i in imgs_text if 'TIF' not in i] # Png next or first jpg
            if not full_res_str:
                full_res_str = [imgs_text[0]] # Whatever is left over

        full_res_idx = imgs_text.index(full_res_str[0])
        img_link = 'https:' + imgs_links[full_res_idx]

        if img_link.split('.')[-1] not in ['jpg','png']:
            print(img_link)
            print(active)
            print(count)
            print(timestamp())
            raise Exception


        count+=1
        if count < 247:
            previous = active
            active = next
        else:
            print(previous)
            break

    print(count)
    print(f'{timestamp()} Done...')


if __name__ == "__main__":
    main()