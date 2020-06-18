# shuowen
updated ancientChinese toolkit

## usage for python file

```
    if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Shuowen Platform.')
    parser.add_argument('-f', '--file', default="../data/test1.docx", help='input docx address')
    parser.add_argument('-m', '--mode', default="docx", help='return in docx or html')
    parser.add_argument('-s', '--style', default="3", help='output with img or id')
    args = parser.parse_args()
    
    tb = tuban(args.file)
    try:
        flag = tb.parse()
        tb.array2dict_save()
    except:
        flag = -2
    if flag == -1:
        if args.mode == "docx":
            tb.dict2order_save()
            tb.get_output_docx_by_docx(args.style)
        elif args.mode == "html":
            tb.dict2order_save()
            tb.get_output_html()
        else:
            print("Wrong Mode")
    else:
        print(tb.get_error())
    # tb.clean_cache()
```

## usage for a util

```
    tb = tuban("path/to/file")
    try:
        flag = tb.parse()
        tb.array2dict_save()
    except:
        flag = -2
    if flag == -1:
        if args.mode == "docx":
            tb.dict2order_save()
            tb.get_output_docx_by_docx(style)
        elif args.mode == "html":
            tb.dict2order_save()
            tb.get_output_html()
        else:
            print("Wrong Mode")
    else:
        print(tb.get_error())
```

## usage for PyQt5

- `tb.get_error()` should be printed out while the document has been analysis
- `file` uploaded should use the same name (rename at the backend)
- `tqdm` should show at the frontend