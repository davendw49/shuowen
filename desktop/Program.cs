using System;
using System.IO;
using System.Text;
using Spire.Doc;
using Spire.Doc.Documents;
using Spire.Doc.Fields;
using System.Collections.Generic;
using System.Collections;

namespace docx_extract
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            //加载文档
            Document document = new Document("../data/test.docx");
            StreamWriter sw = new StreamWriter("names.txt");
            //int j = 1;
            //遍历文档的所有section
            foreach (Section sec in document.Sections)
            {
                //遍历section中的所有段落
                foreach (Paragraph para in sec.Paragraphs)
                {
                    List<DocumentObject> pictures = new List<DocumentObject>();
                    List<DocumentObject> para_obj = new List<DocumentObject>();
                    foreach (DocumentObject docObj in para.ChildObjects){
                        para_obj.Add(docObj);
                    }
                    Console.WriteLine(para_obj.Count);
                    //遍历段落中的所有子元素
                    for (int i=0; i<para_obj.Count;i++){
                        int index = para.ChildObjects.IndexOf(para_obj[i]);
                        int j=i+1;
                        if(para_obj[i].DocumentObjectType ==DocumentObjectType.TextRange ){
                            TextRange textrange =(TextRange) para_obj[i];
                            Console.WriteLine(textrange.Text);
                            String stext = textrange.Text;
                            if (stext.Length!=1){
                                Console.WriteLine(index.ToString()+"处文字连在一起");
                                sw.WriteLine(index.ToString()+"处文字连在一起");
                            }
                            else if(para_obj[j].DocumentObjectType ==DocumentObjectType.Picture){
                                    continue;
                            }else{
                                Console.WriteLine(index.ToString()+"处有错误");
                                sw.WriteLine(index.ToString()+"处有错误");
                            }
                            //Console.WriteLine(stext.Length);
                        }
                        if(para_obj[i].DocumentObjectType == DocumentObjectType.Picture){
                            pictures.Add(para_obj[i]);
                            Console.WriteLine("?");
                            if(para_obj[j].DocumentObjectType == DocumentObjectType.TextRange){
                                continue;
                            }else if(para_obj[j].DocumentObjectType == DocumentObjectType.Picture){
                                Console.WriteLine(index.ToString()+"图片连在一起");
                                sw.WriteLine(index.ToString()+"图片连在一起");
                            }
                        }
                    }
                    sw.Close();
                    foreach (DocumentObject pic in pictures)
                        {
                            //获取图片的位置（index）
                            int index =para.ChildObjects.IndexOf(pic);
                            //插入文本到图片位置
                            TextRange range = new TextRange(document);
                            range.Text = string.Format("?");
                            para.ChildObjects.Insert(index, range);
                            //删除图片
                            para.ChildObjects.Remove(pic);
                            //j++;
                        }
                }
            }
            //保存文档
            document.SaveToFile("11re.docx", FileFormat.Docx);
        }
    }
}
