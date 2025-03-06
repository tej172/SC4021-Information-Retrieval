import praw
import json
from sentence_transformers import SentenceTransformer, util
import pickle
import os

CLIENTID = 
CLIENTSECRET = 
USERAGENT =  # this any be any, just so that enable reddit to track usage
QUERY_EMBEDDING_FILE = "query_embedding.pkl"

def ComputeSimilarity(text):
        # Compute similarity between post and query
        post_embedding = model.encode(text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, post_embedding).item()
        return similarity
reddit = praw.Reddit(
    client_id=CLIENTID,
    client_secret=CLIENTSECRET,
    user_agent=USERAGENT
)


# Choose subreddit
#subReddit = "AskReddit" 
# Search for posts related to "AI replace jobs"
query = "Thoughts on AI replacing jobs"
# Load SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Check if query embedding is already saved
if os.path.exists(QUERY_EMBEDDING_FILE):
    with open(QUERY_EMBEDDING_FILE, "rb") as f:
        query_embedding = pickle.load(f)
    print("Loaded query embedding from file.")
else:
    query_embedding = model.encode(query, convert_to_tensor=True)
    with open(QUERY_EMBEDDING_FILE, "wb") as f:
        pickle.dump(query_embedding, f)
    print("Computed and saved query embedding.")

subRedditList = ['Futurology','ArtificialInteligence','AskReddit','OpenAI','jobs','Economics','careerguidance','singularity','Automate','WorkReform','artificial']
overallRecords = []
overallPosts = 0
overallComments = 0

for subReddit in subRedditList:
    # Fetch posts
    subreddit = reddit.subreddit(subReddit)
    totalComments = 0
    totalPosts = 0
    records = []
    
    for post in subreddit.search(query, limit=None):  # `None` tries to get max available (~1000)
        # Compute similarity between postText and query
        similaritySelfText = ComputeSimilarity(post.selftext)

        # Compute similarity between postTitle and query
        similarityTitle = ComputeSimilarity(post.title)

        # Keep post if similarity is high (Threshold: 0.5)
        if similaritySelfText > 0.5 or similarityTitle > 0.5:
            if post.selftext:
                post_data = {
                    "text": post.selftext,
                    "created_at": post.created_utc,
                    "score": post.score
                }
                records.append(post_data)
                totalPosts +=1
            else:
                post_data = {
                    "text": post.title,
                    "created_at": post.created_utc,
                    "score": post.score
                }
                records.append(post_data)
                totalPosts +=1
            # Fetch and filter top-level comments
            post.comments.replace_more(limit=0)  # Remove "load more" comments
            for comment in post.comments.list():
                if comment.body and comment.body.lower() not in ['[deleted]', '[removed]']:
                    # Compute similarity between comment and query
                    similarityComments = ComputeSimilarity(comment.body)

                    # Keep comment if similarity is high
                    if similarityComments > 0.5:
                        comments_data = {
                            "text": comment.body,
                            "created_at": comment.created_utc,
                            "score": comment.score
                        }
                        records.append(comments_data)
                        totalComments += 1
    overallPosts +=totalPosts
    overallComments +=totalComments            
    # Save to JSON
    with open(f"{subReddit}.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    print(f"r/{subReddit} - Total Records: {len(records)} (Filtered Posts: {totalPosts}, Filtered Comments: {totalComments})")
    
    overallRecords.extend(records)
    
# Save to JSON
with open(f"OverallRecords.json", "w", encoding="utf-8") as f:
    json.dump(overallRecords, f, indent=4)

print(f"OverallRecords - Total Records: {len(overallRecords)} (Filtered Posts: {overallPosts}, Filtered Comments: {overallComments})")


# https://www.reddit.com/r/Futurology/search/?q=Ai+replace+jobs&cId=2bb9276a-850f-4626-b47b-50a9a039831d&iId=25221d89-92f3-458b-a701-ce057e53405f -> post: 214, total comments: 35755
# https://www.reddit.com/r/ArtificialInteligence/search/?q=ai+replace+job&cId=0cff5038-a982-4eab-8a1b-10cf8e3dd557&iId=2d00f3fd-4001-42eb-9214-a6f3a23cec5f -> post: 234, total comments: 13685
# https://www.reddit.com/r/AskReddit/search/?q=ai+replace+job&cId=efefb538-b0d5-4bac-a522-d4ca6bdf37c4&iId=2c25225d-125a-4804-9466-ba83d650c0a6 -> post: 219, total comments: 4262
# https://www.reddit.com/r/OpenAI/search/?q=ai+replace+job&cId=be760b25-7efd-40d6-814c-c278b5045a4d&iId=1f44d686-b866-4789-89a6-c126b17dd58d -> post: 232, total comments: 15098
# https://www.reddit.com/r/jobs/search/?q=ai+replace+job&cId=e2a6ce98-1d64-4262-acdd-0f8993ee4d5e&iId=2ea29ade-7bfd-4d6d-b1d1-6a503c41882b -> post: 236, total comments: 13638
# https://www.reddit.com/r/Economics/search/?q=AI+replacing+jobs&cId=894eb197-8b46-416c-9cbf-60ef1e78a7a2&iId=342cee5c-70cf-4c30-b196-7cf55ba7340c -> post: 103, total comments: 6413
# https://www.reddit.com/r/careerguidance/search/?q=AI+replacing+jobs&cId=99562e91-3730-49d3-a2e6-44c5d65dfdfc&iId=83a34f10-8b52-4c01-9fc7-50bfff30522d -> post: 230, total comments: 6912
# https://www.reddit.com/r/singularity/search/?q=AI+replacing+jobs&cId=ddb163c5-2f5f-445c-82bc-194f2c78c161&iId=ea476518-f627-4da3-b857-1e89fe3b5b56 -> post: 224, total comments: 30370
# https://www.reddit.com/r/Automate/search/?q=AI+replacing+jobs&cId=3aade0a7-e5ca-4f23-a996-89b82686bb0a&iId=9a19df74-2c34-4d56-b410-e6d474c984ea -> post: 195, total comments: 2004
# https://www.reddit.com/r/WorkReform/search/?q=AI+replacing+jobs&cId=6b6dcdbb-c804-4877-bf2e-37f40c18c497&iId=61b79b81-28e3-43c3-955f-3b8ca22f0304 -> post: 230, total comments: 7391
# https://www.reddit.com/r/antiwork/search/?q=AI+replacing+jobs&cId=7145dc72-32b4-40b7-9b92-cca84162abcf&iId=08b61ba8-64fa-4727-9d66-4d24f2f26b66 -> post: 223, total comments: 43621
# https://www.reddit.com/r/Advice/search/?q=AI+replacing+jobs&cId=c97745ba-1f7d-411e-a6de-5ef0a377342c&iId=dfd144b1-2047-4a43-93a0-bc107908458c -> post: 229, total comments: 3547
# https://www.reddit.com/r/worldnews/search/?q=AI+replacing+jobs&cId=e6b1fabf-5149-4d6a-b87e-170f6fa6e2aa&iId=6528802c-ad12-407f-9e48-7a1f8de47b93 -> post: 61, total comments: 4534
# https://www.reddit.com/r/artificial/search/?q=AI+replacing+jobs&cId=441d296a-e32c-453e-9480-e680dbde7239&iId=f020b83f-07b1-4a32-81ad-c74ff4d6949a -> post: 235, total comments: 8541


# 


'''
Query: AI replacing jobs
r/Futurology - Total Records: 1212 (Filtered Posts: 84, Filtered Comments: 1128)
r/ArtificialInteligence - Total Records: 2716 (Filtered Posts: 117, Filtered Comments: 2599)
r/AskReddit - Total Records: 12 (Filtered Posts: 4, Filtered Comments: 8)
r/OpenAI - Total Records: 489 (Filtered Posts: 42, Filtered Comments: 447)
r/jobs - Total Records: 143 (Filtered Posts: 7, Filtered Comments: 136)
r/Economics - Total Records: 14 (Filtered Posts: 3, Filtered Comments: 11)
r/careerguidance - Total Records: 180 (Filtered Posts: 5, Filtered Comments: 175)
r/singularity - Total Records: 2617 (Filtered Posts: 99, Filtered Comments: 2518)
r/Automate - Total Records: 30 (Filtered Posts: 18, Filtered Comments: 12)
r/WorkReform - Total Records: 10 (Filtered Posts: 3, Filtered Comments: 7)
r/artificial - Total Records: 472 (Filtered Posts: 69, Filtered Comments: 403)
OverallRecords - Total Records: 7895 (Filtered Posts: 451, Filtered Comments: 7444)
'''
