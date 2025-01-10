# instagram_media_downloader
> Python script to download locally all the media from an instagram account
  
# Steps:
1. You need a Business App on https://developers.facebook.com/
2. You need to add the Instagram API to your app.
3. Retrieve the USER_ID and ACCESS_TOKEN by linking a creator or business ig account to your app.
4. Store those variables into a .env file in the root of your project.
5. create a virtual environment using venv `python -m venv name_of_venv_folder`
6. install all the dependencies from the requirement.txt file `pip install -r requirements.txt`
7. execute the script `python -m instagram_media_downloader` and wait till all the media are downloaded into the `/instagram_media` folder.
