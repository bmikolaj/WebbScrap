from datetime import datetime
from pyquery import PyQuery as pquery

import urllib3
urllib3.disable_warnings()

import webbrowser

def timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def main():
    active = 'https://webbtelescope.org/contents/media/images/2022/028/01G77Q8BTTSEB7ZSB2ZEY49HSQ'

    print(f'{timestamp()} Starting...')

    count=0
    while (active):
        py = pquery(active, verify=False)
        page_num = int([i.text() for i in py.find("div.controls").parent().find('li').items()][0])

        span = py.find("span")
        spans = [i.text() for i in span.items()]

        try:
            next_idx = spans.index("Next")
            next = 'https://webbtelescope.org' + [i.attr("href") for i in span.eq(next_idx).parent().items()][0]
        except ValueError:
            if page_num == 247:
                pass
            else:
                print(active)
                print(page_num)
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

        webbrowser.open(img_link)

        count+=1
        if page_num < 247:
            active = next
        else:
            break

    print(f'{timestamp()} Done...')


if __name__ == "__main__":
    main()