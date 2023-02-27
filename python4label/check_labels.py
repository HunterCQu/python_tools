import os

img_formats = ['.bmp', '.jpg', '.jepg', '.png', '.tif', '.dng']

def check_labels(file_path, save_txt):
    i = 0
    with open(save_txt, "w") as st:
        with open(file_path, "r") as f:
            img_files = [x.replace('/', os.sep) for x in f.read().splitlines() if os.path.splitext(x)[-1].lower() in img_formats]
            label_files = [x.replace("images", "labels").replace(os.path.splitext(x)[-1], ".txt") for x in img_files]

            for lf in label_files:

                print(lf)
                with open(lf, 'r') as t:
                    lines = t.readlines()
                    for li in lines:
                        if li.strip().split(" ")[0] == "1":
                            st.write(lf+'\n')
                            break
                            #exit()
    print(i)
    


if __name__ == "__main__":
    file_path = "/data1/workspace_hunter/data/train/new_trian/has/train_0223.txt"
    save_txt = "./error.txt"
    check_labels(file_path, save_txt)

