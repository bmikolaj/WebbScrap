from pyquery import PyQuery as pquery

import urllib3
urllib3.disable_warnings()


def main():
    active = 'https://webbtelescope.org/contents/media/images/2022/028/01G77Q8BTTSEB7ZSB2ZEY49HSQ'

    count=0
    #while (count=0):
    while (active != 'https://webbtelescope.org'):
        py = pquery(active, verify=False)

        span = py.find("span")
        spans = [i.text() for i in span.items()]
        next_idx = spans.index("Next")
        next = 'https://webbtelescope.org' + [i.attr("href") for i in span.eq(next_idx).parent().items()][0]


        imgs_text = [i.text() for i in py.find('a').items()]
        imgs_links = [i.attr('href') for i in py.find('a').items()]
        full_res_str = [i for i in imgs_text if i.startswith('Full') and 'TIF' not in i]

        if len(full_res_str)>1:
            print(active)
            quit(0)

        try:
            full_res_idx = imgs_text.index(full_res_str[0])
        except IndexError:
            print(active)
            print(count)
            raise

        img_link = 'https:' + imgs_links[full_res_idx]

        count+=1
        active = next

    print(count)


if __name__ == "__main__":
    main()