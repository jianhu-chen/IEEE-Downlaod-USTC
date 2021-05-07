import os, tqdm, sys

print("\n".join([
    "使用方法: python rename.py txt_file_path",
    "例如: python rename.py ./ICRA2020.txt",
    "="*30
]))

assert len(sys.argv) == 2, sys.argv

path = sys.argv[1]
with open(path, "r") as f:
    contents = f.read()

infos = {}

contents = contents.split("\n\n")
for one_paper in contents:
    infos_i = one_paper.split("\n")
    doi = "0{}".format(infos_i[1].split(".")[-1])
    name = "".join(infos_i[0].split("\"")[1:-1])
    infos[doi] = {
        "doi": doi,
        "name": name
    }
    assert name.endswith(","), name

print(len(infos.keys()))

src_dir = os.path.abspath("./downloads")

os.makedirs(src_dir, exist_ok=True)

for doi, infos in tqdm.tqdm(infos.items()):
    src = os.path.join(src_dir, "{}.pdf".format(doi))
    name = infos["name"][:-1].replace("/", "|")  # remove ,
    dst = os.path.join(src_dir, "{name}_{doi}.pdf".format(name=name, doi=doi))
    try:
        os.rename(src, dst)
    except Exception as e:
        print(e)

print("Done!")
