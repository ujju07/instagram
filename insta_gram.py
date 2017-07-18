# _______________________________________________________________________________________________
# ****************************************|    INSTABOT     |************************************
# -----------------------------------------------------------------------------------------------


# Here we imported Requests library to make network requests
import requests

# Instagram API Access_token of the owner << used in the scope of basic, public_content, likes ,comments >>
APP_ACCESS_TOKEN = '3757625810.f653a03.8c68a226a37f4ff6a9eb47bdbd539611'
# Base URL common for all the requests in the file.
BASE_URL = 'https://api.instagram.com/v1/'


# Function below is to check whether we have succeeded or not.
def success_or_failure(data):
    print "\n************************************************************************************************"
    if data['meta']['code'] == 200:
        print "Your task was successfully performed."
    else:
        print "Sorry!!!\nYou faced an error while performing your task.\nTry again later!"


# The function below gets the information about the owner of the access_token() using 'GET'.
def owner_info():
    request_owner_url = BASE_URL + "users/self/?access_token=" + APP_ACCESS_TOKEN
    info_of_owner = requests.get(
        request_owner_url).json()  # GET call to fetch the information of the access_token's owner
    print "Full Name                :", info_of_owner["data"]["full_name"]
    print "UserName                 :", info_of_owner["data"]["username"]
    print "User Id                  :", info_of_owner["data"]["id"]
    print "Total Media              :", info_of_owner["data"]["counts"]["media"]
    print "Follows                  :", info_of_owner["data"]["counts"]["follows"]
    print "Followed by              :", info_of_owner["data"]["counts"]["followed_by"]
    print "Link to profile picture  :", info_of_owner["data"]["profile_picture"]
    if info_of_owner['data']['website'] != "":  # If Website of the owner is mentioned
        print "Website                  :", info_of_owner["data"]["website"]
    if info_of_owner['data']['bio'] != '':  # If Bio of the owner is mentioned
        print "Bio                      :", info_of_owner["data"]["bio"]


# The function below gets the information about the User.
def display_user_info(username):
    request_user_url = BASE_URL + "users/search?q=" + username + "&access_token=" + APP_ACCESS_TOKEN
    user_info = requests.get(request_user_url).json()  # GET call to search user for the information
    print "\nFull Name                :", user_info["data"][0]["full_name"]
    print "UserName                 :", user_info["data"][0]["username"]
    print "User Id                  :", user_info["data"][0]["id"]


# The function below gets the information about the User and return user's ID using 'GET'.
def get_user_id(username):
    request_user_url = BASE_URL + "users/search?q=" + username + "&access_token=" + APP_ACCESS_TOKEN
    user_info = requests.get(request_user_url).json()  # GET call to fetch user for the information
    user_id = user_info["data"][0]["id"]
    return user_id  # To Return user's id


# The function below fetches public post starting from the most recent one published by the user using 'GET'.
def get_user_post(username):
    user_id = get_user_id(username)  # get_user_id(username) function called here to get the user's ID
    user_url = BASE_URL + "users/" + user_id + "/media/recent/?access_token=" + APP_ACCESS_TOKEN
    request_user_recent_post = requests.get(user_url).json()  # GET call to fetch user's post
    return request_user_recent_post


# The function below chooses the post in a creative way
# i.e the one with minimum/maximum no. likes/comments or most recent one.
def get_post_by_choice(username, option=0, selection=0, n=0):
    requested_post = get_user_post(username)  # This function is called here to get the user's post details.
    post_index = 0  # For most recent post
    like_list_on_each_post = []
    comment_list_on_each_post = []
    total_user_media = len(requested_post['data'])  # To get the total no. of media
    if total_user_media == 0:
        print("\nThis User has no post!")
    else:
        if option == 1:  # For liking a post
            for each_media in range(0, total_user_media):
                like_list_on_each_post.append(requested_post['data'][each_media]['likes']['count'])
            if selection == 1:  # If we want least liked post to be liked
                least_count = min(like_list_on_each_post)
                post_index = like_list_on_each_post.index(least_count)
            if selection == 3:  # If we want most popular post to be liked
                most_count = max(like_list_on_each_post)
                post_index = like_list_on_each_post.index(most_count)
            if selection == 4:  #For liking all the posts
                post_index = n
        if option == 2:  # For commenting on a post
            for each_media in range(0, total_user_media):
                comment_list_on_each_post.append(requested_post['data'][each_media]['comments']['count'])
            if selection == 1:  # If we want to commented on least commented post
                least_count = min(comment_list_on_each_post)
                post_index = comment_list_on_each_post.index(least_count)
            if selection == 3:  # If we want to comment on most commented post
                most_count = max(comment_list_on_each_post)
                post_index = comment_list_on_each_post.index(most_count)
        print "Link to the Media        :", requested_post['data'][post_index]['link']  # To print the link to a media.
        post_id = requested_post["data"][post_index]['id']
        return post_id  # To return the particular media ID


# The function below sets a like on a particular media by the currently authenticated user using 'post'.
def like_user_post(username, option, selection, n):
    post_id = get_post_by_choice(username, option, selection, n)  # get_user_post_id()function called here to get postID
    like_post_url = BASE_URL + "media/" + post_id + "/likes"
    payload = {'access_token': APP_ACCESS_TOKEN}
    like = requests.post(like_post_url, payload).json()  # Post call to like the post
    success_or_failure(like)  # To check whether we have succeeded or not.


# The function below creates a comment on a media object using 'post'.
def post_comment(username, option, selection):
    media_id = get_post_by_choice(username, option,
                                  selection)  # get_user_post_id(username) function called here to get post ID
    url_post_comment = BASE_URL + "media/" + media_id + "/comments"
    input_comment = raw_input("Write a comment you want to post.\n")
    request_data = {"access_token": APP_ACCESS_TOKEN, 'text': input_comment}  # Required to created a comment.
    comment = requests.post(url_post_comment, request_data).json()  # Post call to comment the post
    success_or_failure(comment)  # To check whether we have succeeded or not.


# The Function returns comment Id that contains a particular word in a particular post
def word_search_in_comment(username, option, selection):
    media_id = get_post_by_choice(username, option,
                                  selection)  # get_user_post_id(username) function called here to get post ID
    url_post_comment = BASE_URL + "media/" + media_id + "/comments?access_token=" + APP_ACCESS_TOKEN
    various_comments = requests.get(url_post_comment).json()
    word_search = raw_input("Enter a word you want to search in the comments")
    print "\n************************************************************************************************"
    comments_id = []
    comments_list = []
    user_name = []
    for each_comment in various_comments['data']:
        comments_list.append(each_comment['text'])
        comments_id.append(each_comment['id'])
        user_name.append(each_comment['from']['username'])
    comments_id_matched = []
    comments_matched = []
    user_found = []
    for each_item in range(len(comments_list)):  # Loop to look for the comment that contains the specified word
        if word_search in comments_list[each_item]:
            comments_matched.append(comments_list[each_item])
            comments_id_matched.append(comments_id[each_item])
            user_found.append(user_name[each_item])
    if len(comments_matched) == 0:  # No comment Found
        print "No comment have " + word_search + " word"
        return False, media_id, False
    else:  # Comment found!
        print "Following are the comments that contains the " + word_search + " word:"
        for i in range(len(comments_matched)):
            print("-->  " + comments_matched[i])
        return comments_id_matched, media_id, comments_matched


# Function to Delete the 1st comment found having a Particular Word.
def delete_comment(username, option, selection):
    user_id = get_post_by_choice(username, option, selection)
    comments_id_matched, media_id, comments_matched = word_search_in_comment(username, option, selection)
    word_to_be_searched = raw_input("Re-Enter the word you searched for so as to delete the comment containing it: ")
    if not comments_id_matched:
        return False
    else:
        for each_item in range(len(comments_id_matched)):
            url = BASE_URL + "media/" + str(media_id) + "/comments/" + str(
                comments_id_matched[each_item]) + "/?access_token=" + APP_ACCESS_TOKEN
            info_to_delete = requests.delete(url).json()  # Delete call to delete comment.
            print "\n************************************************************************************************"
            if info_to_delete['meta']['code'] == 200:
                print "\"" + comments_matched[each_item] + "\" --> deleted"
                print "Your task was successfully performed."
                break
            elif info_to_delete['meta']['error_message'] == "You cannot delete this comment":  # By Default Error
                print comments_matched[each_item], " = ", info_to_delete['meta']['error_message']
            else:
                print "Sorry!!!\nYou faced an error while performing your task.\nTry again later!"


# Function to find Average Number of Words per Comment
def average_words_per_comment(username, option, selection):
    user_id = get_user_id(username)
    post_id = get_post_by_choice(username, option, selection)
    url = BASE_URL + "media/" + post_id + "/comments/?access_token=" + APP_ACCESS_TOKEN
    fetch_info = requests.get(url).json()  # GET call to fetch all the comments
    print "\n************************************************************************************************"
    if len(fetch_info['data']) == 0:  # If no comment on that post by you..
        print("There is no comment on this post.")
    else:
        list_of_comments = []
        word_count = 0
        comments_id = []
        for comment in fetch_info['data']:
            list_of_comments.append(comment['text'])
            word_count += len(comment['text'].split())
            comments_id.append(comment['id'])
        average_words = float(word_count) / len(list_of_comments)  # Formula to calculate average
        print "\nAverage number of words per comment in post = %.2f" % average_words


# The main function to run the entire program...
def main_function():
    print "**************************| _/\_ WELCOME TO INSTABOT SERVICES _/\_ |****************************"
    print "________________________________________________________________________________________________"
    print "\n**************************************| OWN DETAILS |*******************************************"
    owner_info()
    print "************************************************************************************************"
    choice = 'yes'
    while choice != 'no':
        users_list = ['dhiman_nitish_017','ujwalrauniyar']  # List of your sandbox users
        to_print_list = [n for n in users_list[0:len(users_list)]]  # To print entire list
        print "Please enter a username from below : "
        print " , ".join(to_print_list)  # To represent list with commas
        user_name = raw_input("\n")
        if user_name not in users_list:  # If user not found in the list
            print "Invalid username"
        else:
            print "**************************************| USER'S DETAILS |****************************************"
            display_user_info(user_name)
            print "************************************************************************************************"
            print "What would you like to do further :?\nPress 1 to Like a post\nPress 2 to Comment on a post"
            print "Press 3 to search a word in the comment in the post of your choice"
            print("Press 4 to delete the 1st comment containing a particular word.")
            print("Press 5 Get the average number of words per comment in post of your choice.")
            option = int(raw_input("Your option: "))
            print "************************************************************************************************"
            if option not in range(1, 6):
                print"Invalid operation \nPlease try again!"
            else:
                print "Which post you would wish to choose :"
                print "press 1 for the one with the least number of it"
                print "press 2 for the one which has been recently uploaded "
                print "press 3 for the one which is the most popular"
                if option == 1:
                    print "press 4 to like all post"
                post_select = int(raw_input("Your option: "))
                if option == 1:
                    if post_select in [1, 2, 3]:
                        like_user_post(user_name, option, post_select, 0)
                    elif post_select == 4:
                        store = get_user_post(user_name)
                        length = len(store['data'])
                        for post in range(0, length):
                            n = post
                            like_user_post(user_name, option, 4, n)  # Here n is to give the post number.
                    else:
                        print"Invalid post chosen \nYour operation will be done on most recent post then"
                else:
                    if post_select not in [1, 2, 3]:
                        print"Invalid post chosen \n"
                    else:
                        if option == 2:
                            post_comment(user_name, option, post_select)
                        if option == 3:
                            word_search_in_comment(user_name, option, post_select)
                        if option == 4:
                            delete_comment(user_name, option, post_select)
                        if option == 5:
                            average_words_per_comment(user_name, option, post_select)
            print "************************************************************************************************"
            print "Do you want to continue?? (yes/no)"
            opt = raw_input().lower()
            if opt == 'yes' or opt == 'y':
                choice = 'yes'
                pass
            elif opt == 'no' or opt == 'n':
                choice = 'no'
            else:
                print "Invalid choice \n"
                print "The program is terminating..."
                break
    print "________________________________________________________________________________________________"
    print("**************************************| THANK YOU |*********************************************")
    # THE END


main_function()  # Main function called here.