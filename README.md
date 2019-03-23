Generating dataset: Scrape the names of actors from IMDb page.Taking 15 pictures of each actor in the movie and 5 pictures for his/her specific look in that movie.

Encode faces: finding location of faces, encoding facial features and storing the dictionary in a pickle file.

Check video: Download video from youtube and checking it frame by frame for faces with many methods use to eliminate effect of missclassification.(only including a name if it occurs in 3 consecutive frames, including a name if it ocurs in more than 1% of total frames etc.)


Install requirements

$ pip install -r requirements.txt


For testing on already trained model (trained for wolf of the wall street)

$ python check_video.py --encodings wolf_of_wall_street.pickle --url "https://www.youtube.com/watch?v=x-51mt2tIVw"

(this might take a few minutes depending on the length of clip)

For training for any movie and then testing

$ python generate_dataset.py -q "name of the movie" -o pathToOutputFolder

$ python encode_faces.py --dataset pathToDataset --encodings encodings.pickle

$ python check_video.py --encodings encodings.pickle --url "youtube url for video clip to be tested"
