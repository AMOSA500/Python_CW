from tkinter import *
from tkinter import Tk, filedialog
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import os, shutil, platform


# Plaftform Path configuration
input_value = platform.system()
path = ""
app_icon = ""
if input_value == "Windows":
    path = "\img"
    app_icon = "\icon_.ico"
else:
    path = "/img"
    app_icon = "/icon_.ico"

# Global Variables
main_file_directory = os.path.dirname(__file__)
filedir = main_file_directory + path
friendImageLabelPathList = []
labelImageFrameList = []
frame_row = 2
image_extension = [".jpg", ".png", ".jpeg", ".bmp"]
label_width=1200
label_height=200
image_size  = 150
x_callback_index = 0
gallery_display_status = False



# Main Image Button Function
def show_image_as_button():
    global filedir,labelFrame_imageButton, label_width, label_height, image_size
    global mainImageButtonList,  gallery_display_status
    r = 0
    mainImageButtonList = []
    
    # File Directory - Select Image Path
    file_list = os.listdir(filedir)
    sorted_file_list = sorted(file_list)

    # LabelFrame to hold Image Buttons
    labelFrame_imageButton = LabelFrame(win,text="Friends Gallery - Click a friend to see their friends",width=label_width,height=label_height,background="#000000",foreground="white")
    labelFrame_imageButton.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky=NW)
    labelFrame_imageButton.grid_propagate(0)

    # Show Images in the main directory
    for file in sorted_file_list:
        (name, ext) = os.path.splitext(file)
        if ext in image_extension:
            img = Image.open(filedir + "/" + file)
            img_resize = img.resize((image_size, image_size), Image.Resampling.LANCZOS)
            profile_image = ImageTk.PhotoImage(img_resize)

            # Image Button 
            # https://www.w3schools.com/python/python_lambda.asp
            imageButton = ttk.Button(
                labelFrame_imageButton,
                text=name.capitalize(),
                style="TButton",
                image=profile_image,
                compound="top",
                cursor="hand2",
                
                command=lambda friend_dir_name=name: show_friends_of_friend(friend_dir_name))
            mainImageButtonList.append(imageButton) # List of all Image Buttons
            imageButton.image = profile_image  # Garbage Collection
            mainImageButtonList[r].pack(side=LEFT)
            r = r + 1
        else:
            pass

    clearAllButton.config(state=NORMAL, style="big.TButton")
    showImageButton.config(state=DISABLED, style="big_disabled.TButton")
    gallery_display_status = True
   
    


# Friends Image Label Function
def show_friends_of_friend(name):
    global friendImageLabelPathList,filedir,frame_row,image_extension,xcloseButton,labelImageFrameList
    global label_width, label_height
    friendsImageLabelList = []
    path = os.path.join(filedir, name + "/")
    r = 0

    if path in friendImageLabelPathList: # Check if Friends Image Label are displayed
        if os.path.isdir(path): # Check if path exist
            file_list = os.listdir(path) # Fetch all 
            if imageInFolderChecker(file_list): # Check if folder contains image
                messagebox.showinfo("Friend Gallery", "This friend's friends are already displayed")
            else:
                messagebox.showinfo("Friend Gallery",f"Folder exist for {name.capitalize()} but no images in the folder",)
        else:
            messagebox.showinfo("Friend Gallery","Missing folder, No images found for " + name.capitalize(),)
    else:
        friendImageLabelPathList.append(path) # Append imageLabel Path to friendImagePathList
        if os.path.isdir(path):
            file_list = os.listdir(path)
            if imageInFolderChecker(file_list): # Check if folder contains images
                # LabelFrame for Image Labels
                imageLabel_labelFrame = LabelFrame(win,text=f"{name.capitalize()} Friends",width=label_width,height=label_height,background="#000000",foreground="white")
                imageLabel_labelFrame.grid(row=frame_row, column=0, columnspan=5, padx=10, pady=10, sticky=NW)
                labelImageFrameList.append(imageLabel_labelFrame)
                imageLabel_labelFrame.grid_propagate(0)

                # Friend Images in the main directory
                for file in file_list:
                    (btn_name, ext) = os.path.splitext(file)
                    if ext in image_extension:
                        img = Image.open(path + file)
                        img_resize = img.resize((120, 120), Image.Resampling.LANCZOS)
                        profile_image = ImageTk.PhotoImage(img_resize)
                        imageLabelOfFriends = ttk.Label(imageLabel_labelFrame,text=btn_name,image=profile_image,background="#000000",foreground="white",)
                        friendsImageLabelList.append(imageLabelOfFriends) # Append all image label to a list
                        imageLabelOfFriends.image = profile_image  # Garbage Collection
                        friendsImageLabelList[r].pack(side=LEFT)
                        r = r + 1
                        frame_row += 1
                    else:
                        pass
                
                # Show 'X' on main image
                for index,value in enumerate(mainImageButtonList): # mainImageButtonList contains all image buttons
                    btn_text = value["text"] # returns the button text value                   
                    if name.lower() == btn_text.lower():
                        # index_val would remember the position of the main image in mainImageButtonList
                        index_val = mainImageButtonList.index(value)

                        # Close Button
                        xcloseButton = Button(imageLabel_labelFrame,text="X",background="#000000",foreground="red",borderwidth=1,)
                        xcloseButton.config(command=lambda: xcloseImageLabel(path, imageLabel_labelFrame,name, index_val))
                        xcloseButton.pack(side=RIGHT, anchor="e")
                        
                        # Disable the selected image button and add X to the center
                        mainImageButtonList[index].configure(state=DISABLED,text="X",compound="center",style="img_disabled.TButton")
            else:
                messagebox.showinfo("Friend Gallery",f"Folder exist for {name} but no images in the folder",)
        else:
            messagebox.showinfo("Friend Gallery", "Missing folder, No images found for " + name.capitalize())



# Check File Extension in a Folder has Image
def imageInFolderChecker(list) -> bool:
    extension_status = False
    for file in list:
        (name, ext) = os.path.splitext(file)
        if ext in image_extension:
            extension_status = True
    return extension_status



# xcloseImageLabel Function
def xcloseImageLabel(path, labelFrame,name,row):
    # Remove X on image
    for value in mainImageButtonList:
        btn_index =mainImageButtonList.index(value)           
        if btn_index == row:
            mainImageButtonList[row].configure(
                state=NORMAL,
                text=name.capitalize(),
                compound="top",
                style="TButton"
                )
    
    friendImageLabelPathList.remove(path)
    labelFrame.destroy()
    


# Clear All
def clear_all():
    global gallery_display_status
    if gallery_display_status:
        # Clear main Image Button
        labelFrame_imageButton.grid_forget()
        # Clear Friend of Friend Image Labels
        for frame in labelImageFrameList:
            frame.destroy()
        # Clear Friends of Friend Image Path from the list
        friendImageLabelPathList.clear()
        # Disable the Clear Button
        clearAllButton.config(state=DISABLED, style="big_disabled.TButton")
        showImageButton.config(state=NORMAL, style="big.TButton")
        gallery_display_status = False
   


# Add New Friend
def addNewFriend():
    global gallery_display_status
    if gallery_display_status:
        new_friend_image = filedialog.askopenfilename(initialdir=main_file_directory,title="Select New Friend to Add")
        (name, ext) = os.path.splitext(new_friend_image)
        if ext in image_extension:
            msgbox = messagebox.askyesno(title="Add a New Friend",message="Do you want to add New Friend or Not?")
            if msgbox:
                shutil.copy(new_friend_image,filedir)
                clear_all()
                show_image_as_button()
            else:
                messagebox.showinfo("New Friend","New Friend Canceled")
        else:
            messagebox.showinfo("Wrong File","The selected file is not an image")
    else:
        messagebox.showinfo("Gallery Status", "Gallery is OFF, you need to show friends first..")


# Delete New Friend
def deleteNewFriend():
    global gallery_display_status
    if gallery_display_status:
        friend_image_to_delete = filedialog.askopenfilename(initialdir=main_file_directory,title="Select New Friend to Delete")
        (name, ext) = os.path.splitext(friend_image_to_delete)
        if ext in image_extension:
            msgbox = messagebox.askyesno(title="Delete Friend",message="Do you want to delete a Friend or Not?")
            if msgbox:
                os.remove(friend_image_to_delete)
                clear_all()
                show_image_as_button()
            else:
                messagebox.showinfo("Delete Friend","Deletion of a Friend Canceled")
    else:
        messagebox.showinfo("Gallery Status", "Gallery is OFF, you need to show friends first.")


# Quit Window
def quit():
    answer = messagebox.askquestion("Confirm","Are you sure you want to quit?")
    if answer == "yes":
        win.destroy()
    else:
        messagebox.showinfo("Information","Continue with Application!")


# Create Window
win = Tk()
win.title("Image File Application")
win.configure(background="#3ae374")
win.iconbitmap(main_file_directory+app_icon)
win.minsize(width=label_width, height=1200)
win.maxsize(width=2000, height=1200)


# Buttons LabelFrame
lframe1 = LabelFrame(win,text="Friends Gallery Menu",width=label_width,height=150,background="#000000",foreground="white",)
lframe1.grid(row=0, column=0, sticky=NW, ipadx=10, ipady=10)
lframe1.grid_propagate(0)

# lframe_canvas


# styling
style = ttk.Style()
style.theme_use("alt")
style.configure(
    "TButton",
    background="#000000",
    foreground="#ffffff",
    width=15,
    borderwidth=1,
    foocusthickness=3,
    focuscolor="#7b8f8a",
)
style.map(
    "TButton",
    background=[("active", "#6d6b6b")],
    foreground=[("active", "white")]
)
style.configure(
    "big.TButton",
    font=(None, 12),
    foreground="#f5dd9d"
)

style.configure(
    "big_disabled.TButton",
    font=(None, 12),
    foreground="grey"
)
style.configure(
    "img_disabled.TButton",
    font=("Arial", 50),
    width=None,
    height=None,
    padding=20,
    foreground="grey"
)



# Create Win Buttons
showImageButton = ttk.Button(lframe1, text="Show Friends", style="big.TButton", command=show_image_as_button)
showImageButton.pack(side=LEFT, expand=1, ipadx=10, ipady=10)

clearAllButton = ttk.Button(lframe1, text="Clear All", style="big.TButton", command=lambda: clear_all())
clearAllButton.pack(side=LEFT, expand=1, ipadx=10, ipady=10)
clearAllButton['state'] = 'disabled'

deleteFriendButton = ttk.Button(lframe1, text="Delete a Friend", style="big.TButton", command=deleteNewFriend)
deleteFriendButton.pack(side=LEFT, expand=1, ipadx=10, ipady=10)

addFriendButton = ttk.Button(lframe1, text="Add New Friend", style="big.TButton", command=addNewFriend)
addFriendButton.pack(side=LEFT, expand=1, ipadx=10, ipady=10)

quitButton = ttk.Button(lframe1, text="Quit", style="big.TButton", command=quit)
quitButton.pack(side=LEFT, expand=1, ipadx=10, ipady=10)


win.mainloop()
