import os
import markdown_it
from deep_translator import GoogleTranslator

def create_folder_and_heading(header, path):
    print(f"FILE {path}")
    print("-"*100)
    folder_path = path.replace(" ", "_")
    os.makedirs(os.path.join("READMES", folder_path), exist_ok=True)
    readme_content = f"# {header}\n"
    with open(os.path.join("READMES", folder_path, "README.md"), "w") as file:
        file.write(readme_content)


def add_to_readme(path, text:str):
    folder_path = path.replace(" ", "_")
    readme_content = f"\n{text}"
    with open(os.path.join("READMES", folder_path, "README.md"), "a+") as file:
        file.write(readme_content)

def add_code_to_readme(path, text, info):
    folder_path = path.replace(" ", "_")
    readme_content = f"\n```{info}\n{text}\n```"
    with open(os.path.join("READMES", folder_path, "README.md"), "a+") as file:
        file.write(readme_content)


# Function to parse the README.md and extract headers and text
def dissect_readme(filename):
    with open(filename, 'r') as file:
        md_text = file.read()

    parser = markdown_it.MarkdownIt()
    tokens = parser.parse(md_text)

    header_level = 0
    heading_text = ""
    heading = False
    directory = ""
    prev_header_level = 0
    readme_content = ""
    bullet_tab = ""

# header = GoogleTranslator(source='zh-CN', target='en').translate(header)
    for token in tokens:
        if token.type == 'heading_open':
            if len(readme_content) > 0:
                add_to_readme(directory, readme_content)
                readme_content = ""
            header_level = int(token.tag[1]) 
            heading = True
        elif token.type == 'heading_close':
            heading = False
        elif token.type == 'inline' and heading:
            print("LEVEL:", header_level)
            print("PREV:", prev_header_level)
            if header_level == 1:
                directory = GoogleTranslator(source='zh-CN', target='en').translate(token.content)
            elif header_level > prev_header_level:
                directory += "/"+GoogleTranslator(source='zh-CN', target='en').translate(token.content)
            else:
                arr = directory.split("/")
                arr[header_level-1] = GoogleTranslator(source='zh-CN', target='en').translate(token.content)
                arr = arr[0:header_level]
                directory = "/".join(arr)
            prev_header_level = header_level
            heading_text = GoogleTranslator(source='zh-CN', target='en').translate(token.content)
            create_folder_and_heading(heading_text, directory)
        else:
            #if len(token.content) > 0:
            content = GoogleTranslator(source='zh-CN', target='en').translate(token.content)
            if token.type == 'fence':
                readme_content += f"```{token.info}\n{content}\n```\n"
                #add_code_to_readme(directory, content, token.info)
            elif token.type == 'bullet_list_open':
                pass
            elif token.type == 'list_item_open':
                bullet_tab = "  "*(token.level-1)+"-"
            elif token.type == 'inline' and len(bullet_tab) > 0:
                readme_content += f"{bullet_tab} {content}\n"
            elif token.type == 'bullet_list_close':
                bullet_tab = ""
            else:
                readme_content += content
                
    add_to_readme(directory, readme_content)
        



if __name__ == "__main__":
    readme_file = "README.md"
    dissect_readme(readme_file)
