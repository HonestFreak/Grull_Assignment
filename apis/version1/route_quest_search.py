from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from fuzzywuzzy import process
from chromadb import chromadb
from db.models.quests import Quest
from db.models.users import User

router = APIRouter()
client = chromadb.PersistentClient(path="/chroma/")

@router.post("/native/")
def native_string_search(
    term: str,
    db: Session = Depends(get_db),
):
    # search for term in quests
    results = db.query(Quest).filter(Quest.description.ilike(f"%{term}%")).all()
    return results

@router.post("/fuzzy/")
async def fuzzy_search(
    term: str,
    db: Session = Depends(get_db),
):
    all_quests = db.query(Quest).all()
    quest_dict = {quest.description: quest for quest in all_quests}
    results = process.extract(term, quest_dict.keys(), limit=10)
    fuzzy_results = [quest_dict[result[0]] for result in results]
    return fuzzy_results

@router.post("/add_to_vector_db/")
def add_to_vector_db(quest_id: int ,db: Session = Depends(get_db))-> None:
    quest = db.query(Quest).filter(Quest.id == quest_id).first()
    collection = client.get_or_create_collection(name="quest") 
    collection.add(
    documents=[quest.description],
    metadatas=[{"id": quest.id , "title": quest.title}],
    ids=[str(quest.id)])

    return {"msg": "Successfully added to vector db."}

@router.post("/search_vector_db/")
def search_chroma(term: str , number_of_results: int, db: Session = Depends(get_db))-> None:
    collection = client.get_or_create_collection(name="quest") 
    results = collection.query(
    query_texts=[term],
    n_results=number_of_results,)

    return results

@router.post("/user_recommendation/")
def user_recommendation(user_id: int, number_of_results: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    recommmendations = set()
    if user:
        print(user.specializations)
        query_texts = list(user.specializations)  # Extract values from the dictionary
        print(query_texts)
        collection = client.get_or_create_collection(name="quest") 
        results = collection.query(query_texts=query_texts, n_results=number_of_results)
        return results
    else:
        return {"msg": "User not found"}