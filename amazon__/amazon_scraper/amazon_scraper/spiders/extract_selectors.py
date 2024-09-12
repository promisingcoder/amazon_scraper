from bs4 import BeautifulSoup as bs
with open('product1.html') as f:
    page1 = f.read()

soup1 = bs(page1,'html.parser')
with open("product2.html") as f:
    page2 = f.read()
soup2 = bs(page2,'html.parser')
all_tags =  set([tag.name for tag in soup1.find_all()])
#unwanted_tags  = ['video','path','noscript','script','form','br','dptags:querylogoperation','style','html','input','button']

#for item in list(all_tags):
    #if item in unwanted_tags:
        #all_tags.remove(item)

def rearrange_tags_according_to_importance(all_tags,piority_tags):
    return [a for a in all_tags if a  in piority_tags] + [a for a in all_tags if a not in piority_tags]

fields1 =  {
    'productTitle' : '        Testa Toro Comfortable Casual Shoes High Sole for Everyday Life - Testa Toro       ',
    'rating' : ' 3.0 ',
    'price' : 'EGP299.00',
    'product_color' : 'aura white',
    'category_product_details' : 'Care instructions',
    'category_product_details_value' : 'Machine Wash',
    'product_description' : 'تركيبة فريدة من نوعه يتمزج بها خليط مميز من مواد التصنيع لوجه الحذاء لدينا هنا قميص أساسية من الألياف المطعم بجلد شمواه السويدي وتططمات أخرى من الجلد المعالجة مع طبين داخلي من فوم المزدوج وكل هذا يقف علي نعل مرتفع عن الأرض ذو كثافة عاليه مزود بفرش من فوم اضا ليعطي مع الشكل المميز تجربة راحة لا تصف',
    'product_details_general' : """Manufacturer
                                    ‏
                                        :
                                    ‎
                                """,
    'review_user_name' : 'Abdo',
    'review_title' : 'متبهدل',
    'review_stars' : '1.0 out of 5 stars',
    'review_product_size' : 'Size: 44 EUColor: beige (clay)',
    'review_product_color' : 'Color: beige (clay)',
    'review_verified_purchase' : 'Verified Purchase',
    'review_date' : 'Reviewed in Egypt on 22 July 2024'
    ,
    'review_found_this_helpful' : '3 people found this helpful',
    'review_details' : """جاي متبهدل و تغليف و الكوتشي كانو مستخدم"""


        }
fields2 = {
    'productTitle' : '        adidas mens GRAND COURT ALPHA Sneaker       ',
    'rating' :  ' 4.4 ',
    'price' : 'EGP4,949',
    'product_color' : 'ftwr white,legend ink,bright royal',
    'category_product_details' : 'Care instructions',
    'category_product_details_value' : 'Hand Wash Only',
    'product_description'  : "The 3-Stripes mean heritage. And when they're placed on these adidas Grand Court Alpha shoes, they celebrate generations of originality. The clean silhouette brings forth that timeless look. An embossed logo on the tongue and upscale stitchwork give everything a modern touch. Cloudfoam brings cushioning that keeps every step a pampered experience.",
    'product_details_general' : """Date First Available
                                    ‏
                                        :
                                    ‎
                                """,
    'review_user_name' : 'djkubi',
    'review_title' : 'Rahat ve Şık',
    'review_stars' : '5.0 out of 5 stars',
    'review_product_size' : 'Size: 42 EUColor: ftwr white,legend ink,bright royal',
    
    'review_verified_purchase' : 'Verified Purchase',
    'review_date' : 'Reviewed in Turkey on 30 July 2024',
    'review_details' : 'Adidas hangi numara giyiyorsam bu numarayı sipariş ettim. Sorunsuz giyiyorum. Çok rahat şık ve dayanıklı bir seri.',

}
def parent(tag):
    return(tag.parent)

all_tags = list(set(all_tags))
def find_parent_selector(Found,tag,found,soup1,soup2,selection_string,item):
    if item == "product_description":
        print("Last 1")
        print(selection_string)
        if item in Found.keys():
            print(Found[item])
    if selection_string.count(" ") > 4:
        return(Found)

    if tag.parent.name == "html" or tag.parent.name == "body" :
        return Found
    parent_attributes  = tag.parent.attrs
    parent = tag.parent
    if item == "product_description":
        print("product_description parent : ")
        print(parent)
    if  not parent_attributes:
        Found =  find_parent_selector(Found,parent,found,soup1,soup2,f"{parent.name} {tag.name}",item)

    for thing1 in parent_attributes:
        if thing1 == "style":
            continue
        
        if thing1 == 'class':
            for class_name in parent_attributes[thing1]:
                if parent_attributes[thing1] == "{}":
                    continue
                selection_string = f"{parent.name}[{thing1}='{class_name}']"+" " + selection_string
                selection_dict = {parent.name : {'class' : class_name}}
                selection = soup1.select(selection_string)
                condition = [a for a in soup2.select(selection_string) if a.text  == fields2[item]]
                
                
                if   len(condition) != 0 and selection:
                                        
                    Found[item] = selection_string
                    break
        else:
            if parent_attributes[thing1] == "{}":
                continue
            selection_string = f"{parent.name}[{thing1}='{parent_attributes[thing1]}']"+" " + selection_string
            selection_dict = {parent.name : {thing1 : parent_attributes[thing1]}}
            selection = soup1.select(selection_string)
            
            condition = [a for a in soup2.select(selection_string) if a.text  == fields2[item]] 

            
            if   len(condition) != 0 and selection:
                                    
                Found[item] = selection_string
                break
            
        if item in Found.keys():
            break
        
        
        
        Found  = find_parent_selector(Found,parent,found,soup1,soup2,selection_string,item)
    
                    
        
        
    return(Found)

def return_selectors(soup1,soup2,all_tags,fields1,fields2):
    
    Found = {}
    
    for _ in all_tags:
       
        if _ == "img":
            #print("found image in 1")
            pass

        for item in fields1:
            if item == "product_description":
                print("1 : ")
                print(item)

            found_condition = False
            if item  == 'review_found_this_helpful':
                continue
            found = soup1.findAll(
    lambda tag: tag.name == _ and
tag.text == fields1[item]
)
            
            if item == "review_product_size":
                pass
                #print(found)
            if item == "product_description":
                print("3 : ")
                print(found)
                if len(found) > 0:
                    print(found[0])
            if len(found) > 0:
                
            
                tag = found[0]
                
                if tag.name == "img":
                    #print("found in 2")
                    #print(tag)
                    pass
                else:
                    pass
                    #print("img not found")
                attributes = tag.attrs
                if item == "product_description":
                    print("attributes of product_description")
                    print(attributes)
                if len(attributes) == 0:
                    print("passed")
                    Found =  find_parent_selector(Found,tag,found,soup1,soup2,tag.name,item)
                for thing in attributes:
                    
                    
                    
                    if found_condition == True:
                        break
                    if tag.name == "img":
                        #print(attributes)
                        pass                    
                    if thing == 'class':
                        pass
                        #print(thing)
                        
                        for class_name in attributes[thing]:
                            selection_string = f"{tag.name}[class='{class_name}']"
                            if tag.name == "img":
                                #print(selection_string)
                                pass                            
                            selection_dict = {tag.name : {'class' : class_name}}
                            if "img" in selection_string:
                                pass
                                #print(selection_string)
                            if item == "review_product_size":
                                #print(selection_string)
                                pass
                            selection = soup1.select(selection_string)
                            
                           
                            condition = [a for a in soup2.select(selection_string) if a.text  == fields2[item] or a.get("alt") == fields2[item]]
                            if tag.name =="img":
                                #print(selection)
                                #print(condition)
                                pass
                            if item == "product_description":
                                print("2 : ")
                                print(selection)
                                print(condition)
                            if   len(condition) > 0 and len(selection) > 0 :
                                
                                
                                Found[item] =  selection_string
                                found_condition = True
                                break
                        

                    else:
                        
                        selection_string = f"{tag.name}[{thing}='{attributes[thing]}']"
                        
                        if attributes[thing] == "{}":
                            continue
                        selection_dict = {tag.name : {thing : attributes[thing]}}
                        selection = soup1.select(selection_string)
                        

                       
                        
                        condition = [a for a in soup2.select(selection_string) ]
                        if item == "review_product_size":
                            #print(selection_string)
                            #print("selection")
                            #print(selection)
                            #print("condition")
                            #print(condition)
                            pass
                        if  len(condition) > 0 and len(selection) > 0 :
                        
                            Found[item] = selection_string
                            found_condition = True
                            
                            break
                    
                  
                        
                        
                    Found =  find_parent_selector(Found,tag,found,soup1,soup2,selection_string,item)
                    

        
                       
                    
                        

                   



                        
    return(Found)

result = return_selectors(soup1,soup2,all_tags,fields1,fields2)
print(len(result))
print(result)

    




            
