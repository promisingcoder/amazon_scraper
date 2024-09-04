from bs4 import BeautifulSoup as bs
with open('product1.html') as f:
    page1 = f.read()

soup1 = bs(page1,'html.parser')
with open("product2.html") as f:
    page2 = f.read()
soup2 = bs(page2,'html.parser')
all_tags =  set([tag.name for tag in soup1.find_all()])
unwanted_tags  = ['video','path','noscript','script','form','br','dptags:querylogoperation','style','html','input','button']

for item in list(all_tags):
    if item in unwanted_tags:
        all_tags.remove(item)

def rearrange_tags_according_to_importance(all_tags,piority_tags):
    return [a for a in all_tags if a  in piority_tags] + [a for a in all_tags if a not in piority_tags]

fields1 =  {
    'productTitle' : '        Testa Toro Comfortable Casual Shoes High Sole for Everyday Life - Testa Toro       ',
    'rating' : '3.0 ',
    'price' : 'EGP299.00',
    'product_color' : 'aura white',
    'category_product_details' : 'Care instructions',
    'category_product_details_value' : 'Machine Wash',
    'about_this_item_item_list' : 'Brand: Testa Toro',
    'product_description' : 'تركيبة فريدة من نوعه يتمزج بها خليط مميز من مواد التصنيع لوجه الحذاء لدينا هنا قميص أساسية من الألياف المطعم بجلد شمواه السويدي وتططمات أخرى من الجلد المعالجة مع طبين داخلي من فوم المزدوج وكل هذا يقف علي نعل مرتفع عن الأرض ذو كثافة عاليه مزود بفرش من فوم اضا ليعطي مع الشكل المميز تجربة راحة لا تصف',
    'product_details_general' : """Manufacturer
                                    ‏
                                        :
                                    ‎
                                """,
    'review_user_name' : 'Abdo',
    'review_title' : 'متبهدل',
    'review_stars' : '1.0 out of 5 stars',
    'review_product_size' : 'Size: 44 EU',
    'review_product_color' : 'Color: beige (clay)',
    'review_verified_purchase' : 'Verified Purchase',
    'review_date' : 'Reviewed in Egypt on 22 July 2024'
    ,
    'review_found_this_helpful' : '3 people found this helpful',
    'review_details' : """جاي متبهدل و تغليف و الكوتشي كانو مستخدم"""


        }
fields2 = {
    'productTitle' : '        adidas mens GRAND COURT ALPHA Sneaker       ',
    'rating' :  '4.4 ',
    'price' : 'EGP4,949',
    'product_color' : 'ftwr white,legend ink,bright royal',
    'category_product_details' : 'Care instructions',
    'category_product_details_value' : 'Hand Wash Only',
    'about_this_item_item_list' : 'LEATHER,SYNTHETICS',
    'product_description'  : """The 3-Stripes mean heritage. And when they're placed on these adidas Grand Court Alpha shoes, they celebrate generations of originality. The clean silhouette brings forth that timeless look. An embossed logo on the tongue and upscale stitchwork give everything a modern touch. Cloudfoam brings cushioning that keeps every step a pampered experience.""",
    'product_details_general' : """Date First Available
                                    ‏
                                        :
                                    ‎
                                """,
    'review_user_name' : 'djkubi',
    'review_title' : 'Rahat ve Şık',
    'review_stars' : '5.0 out of 5 stars',
    'review_product_size' : 'Size: 45 1/3 EU',
    'review_product_color' : 'Color: silver pebble,silver pebble,olive strata',
    'review_verified_purchase' : 'Verified Purchase',
    'review_date' : 'Reviewed in Turkey on 30 July 2024',
    'review_details' : 'Adidas hangi numara giyiyorsam bu numarayı sipariş ettim. Sorunsuz giyiyorum. Çok rahat şık ve dayanıklı bir seri.',

}
def parent(tag):
    return(tag.parent)

all_tags = list(set(all_tags))
def find_parent_selector(Found,tag,found,soup1,soup2,selection_string,item):
    n = 0
    parent_attributes  = tag.parent.attrs
    parent = tag.parent
    for thing1 in parent_attributes:
        if thing1 == 'class':
            for class_name in parent_attributes[thing1]:
                selection_string = f"{parent.name}[{thing1}='{class_name}']"+" > " + selection_string
                selection = soup1.select(selection_string)
                condition = len([a for a in soup2.select(selection_string) if a.text  == fields2[item]]) == 0
                if len(selection) == len(found) and not condition:
                                        
                    Found[item] = selection_string
                    break
        else:
            
            selection_string = f"{parent.name}[{thing1}='{parent_attributes[thing1]}']"+" > " + selection_string
            selection = soup1.select(selection_string)
            condition = len([a for a in soup2.select(selection_string) if a.text  == fields2[item]]) == 0
            if len(selection) == len(found) and not condition:
                                    
                Found[item] = selection_string
                break

        if item in Found.keys():
            break
        print("Found before")
        print(Found)
        Found2 = find_parent_selector(Found,parent,found,soup1,soup2,selection_string,item)
        for key in Found2.keys():
            Found[key] = Found2[key]
        print("Found_after")
        print(Found)            
        
        
    return(Found)
def return_selectors(soup1,soup2,all_tags,fields1,fields2):
    selector_list = []
    Found = {}
    for _ in all_tags:
        condition = False
        for item in fields1:
            if item  == 'review_found_this_helpful':
                continue
            found = soup1.findAll(
                    lambda tag:tag.name == _ and
                    tag.text ==  fields1[item])
            
            if found:
            
                tag = found[0]
                attributes = tag.attrs
                for thing in attributes:
                    if thing == 'class':
                        for class_name in attributes[thing]:
                            selection_dict = {thing:  class_name}
                            selection = soup1.find_all(tag.name,selection_dict)
                            condition = len([a for a in soup2.find_all(tag.name) if a.text  == fields2[item]]) == 0
                            if len(selection) == len(found) and not condition:
                                
                                
                                Found[item] = {'tag' : f'{tag.name}','selection' :  selection_dict}
                                break
                        

                    else:
                        
                        selection_string = f"{tag.name}[{thing}='{attributes[thing]}']"
                        selection = soup1.select(selection_string)
                        condition = len([a for a in soup2.select(selection_string) if a.text  == fields2[item]]) == 0
                        if len(selection) == len(found) and not condition:
                        
                            Found[item] = selection_string
                            break
                    
                    Found =  find_parent_selector(Found,tag,found,soup1,soup2,selection_string,item)
                        

                   



                        
    return(Found)

print(return_selectors(soup1,soup2,all_tags,fields1,fields2))

    




            
