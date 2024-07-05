from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import db.schemas as schemas
from auth.authorization import get_current_user
from db.database import get_db
import db.models as models

router = APIRouter()


# TODO czy dodawać to zabezpieczenie czterema cyframi?
@router.post('/{mountain_id}', status_code=status.HTTP_201_CREATED)
async def user_unlocks_mountain(mountain_id: str, current_user: Annotated[schemas.User, Depends(get_current_user)],
                                           db: Session = Depends(get_db)):
    user_id = current_user.user_id
    to_add = models.Users_Mountains(user_id=user_id, mountain_id=mountain_id)
    db.add(to_add)
    db.commit()
    db.refresh(to_add)
    
    user_mountains = db.query(models.Users_Mountains).filter(models.Users_Mountains.user_id == user_id).all()

    user_achievements = db.query(models.Users_Achievements).filter(models.Users_Achievements.user_id == user_id).all()

    achievements = db.query(models.Achievements).all()
    
    user_achievement_ids = {achievement.achievement_id for achievement in user_achievements}

    not_achieved = [achievement for achievement in achievements if achievement.achievement_id not in user_achievement_ids]

    achievements_to_add = []
    for ach in not_achieved:
        if str(ach.achievement_id) == "5da013f0-cf1a-4f61-a4a5-7106365c57af": # Zdobywca
            if len(user_mountains) == 28:
                achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))
        if str(ach.achievement_id) == "488fb442-a713-4640-ac6d-0c0c6292377a":# Najłatwiejsze już za tobą
            for mountain in user_mountains:
                if str(mountain.mountain_id) == "0272834d-2a43-411a-bfb1-b90239513491":
                    achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))
                    break
        if str(ach.achievement_id) == "4f9c2ca0-ee9f-4a8a-871a-4c504d7d3a9b":# Wyżej już się nie da
            for mountain in user_mountains:
                if str(mountain.mountain_id) == "cef62e48-bbd1-4128-8aa5-139845070dfc":
                    achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))
                    break
        if str(ach.achievement_id) == "bbd0a19c-83a9-4022-9504-234d0815a2b6":# Zdobądź wszystkie w Sudetach
            # Sudety = ["Ślęża", "Skopiec", "Kłodzka Góra", "Chełmiec", "Biskupia Kopa", "Szczeliniec Wielki", "Waligóra", "Skalnik", "Jagodna",
            #  "Kowadło", "Wielka Sowa", "Orlica", "Rudawiec", "Wysoka Kopa", "Śnieżnik", "Śnieżka"]
            sudety = ["cfe4d9bc-6790-4268-802a-47f48a3904cc", "3bd597dd-95ec-4b6a-b7f1-7b2370c65ca3", "685d2ab6-221c-4659-b146-5e240fa22a8e",
                      "c97af7f6-8d36-4674-8d6e-18a7023cfef8", "2bb31a0b-2332-48ec-8676-2331e2f9cad0", "b939a070-af06-4831-9727-14421c269a10",
                      "990b80e3-1e90-48f0-a78f-8871580f7a09", "e5dc6302-5f16-4c71-a282-ecf93393efaa", "f54d011e-7d27-4b9d-9b83-211d532d84e3",
                      "9a849d45-5b6e-417f-8e49-08ea9d4e75b9", "e7beaeea-a4d4-403f-bed9-e7b02f1abc51", "2c2897d4-4710-4435-9d7f-c5355f6e1819",
                      "892ae3fe-e9e3-434b-be46-3ee795f0619c", "7acd24a7-348b-41a3-9d79-8b159e45b9cd", "bf2dad52-59d0-4638-9625-0e2ab0d9289d",
                      "b5b750db-9036-49b4-a851-84d375a16b40"]
            counter = 0
            for mountain in user_mountains:
                if str(mountain.mountain_id) in sudety:
                    counter += 1   
            if counter == len(sudety):
                achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))         
        if str(ach.achievement_id) == "8f6ac1f2-a88f-466e-97b6-ba458dcc0bbe":# Zdobądź wszystkie w karpatach
            # Karpaty = ["Lubomir", "Czupel", "Lackowa", "Wysoka", "Mogielica", "Skrzyczne", "Radziejowa", "Turbacz", "Tarnica", "Babia Góra", "Rysy"]
            karpaty = ['443fde7d-5958-45c1-9d97-70368e5769e4', 'fbc30a1e-4a39-436c-bc94-44fd2452d54e', '0203d577-a491-4e55-8f0f-8ffeffe20d82',
                    '108b5e52-2f46-40d9-894e-21b8d608fd0d', 'd94917c4-c41a-4ee6-ae3e-a376810b050b', '1fa02214-527e-4f4c-b233-754e38559f43',
                    'f81d3727-9e2f-4e0a-a9af-28bfaf89784f', '4d1e48c9-3ac7-4358-ba09-458e67e6b1f5', '4d74444a-530c-495b-bdb2-ffce3348c0a1',
                    '888fdb22-d598-47f4-9bb9-a40bc893b75d', 'cef62e48-bbd1-4128-8aa5-139845070dfc']
            counter = 0
            for mountain in user_mountains:
                if str(mountain.mountain_id) in karpaty:
                    counter += 1   
            if counter == len(karpaty):
                achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))     
        if str(ach.achievement_id) == "16fa5a46-b2a8-4bae-afe8-c69a2e1d6181":# Powyżej 1000 m p.w.m.
            # above_thousand = ["Wysoka", "Skrzyczne", "Orlica", "Turbacz", "Tarnica", "Wysoka Kopa", "Babia Góra", "Rudawiec", "Śnieżka", "Śnieżnik", "Rysy", "Mogielica", "Wielka Sowa", "Radziejowa"]
            above_thousand = ["108b5e52-2f46-40d9-894e-21b8d608fd0d", "1fa02214-527e-4f4c-b233-754e38559f43", "2c2897d4-4710-4435-9d7f-c5355f6e1819",
                              "4d1e48c9-3ac7-4358-ba09-458e67e6b1f5", "4d74444a-530c-495b-bdb2-ffce3348c0a1", "7acd24a7-348b-41a3-9d79-8b159e45b9cd",
                              "888fdb22-d598-47f4-9bb9-a40bc893b75d", "892ae3fe-e9e3-434b-be46-3ee795f0619c", "b5b750db-9036-49b4-a851-84d375a16b40",
                              "bf2dad52-59d0-4638-9625-0e2ab0d9289d", "cef62e48-bbd1-4128-8aa5-139845070dfc", "d94917c4-c41a-4ee6-ae3e-a376810b050b",
                              "e7beaeea-a4d4-403f-bed9-e7b02f1abc51", "f81d3727-9e2f-4e0a-a9af-28bfaf89784f"]
            counter = 0
            for mountain in user_mountains:
                if str(mountain.mountain_id) in above_thousand:
                    counter += 1   
            if counter == len(above_thousand):
                achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))          
        if str(ach.achievement_id) == "09ce47e9-5bf9-4255-9403-82c692a1bc0d":# Poniżej 1000 m p.w.m.
            # below_thousand = ["Lackowa", "Łysica", "Biskupia Kopa", "Skopiec", "Lubomir", "Kłodzka Góra",
            #  "Waligóra", "Kowadło", "Szczeliniec Wielki", "Chełmiec", "Ślęża", "Skalnik", "Jagodna", "Czupel"]
            below_thousand = ['0203d577-a491-4e55-8f0f-8ffeffe20d82', '0272834d-2a43-411a-bfb1-b90239513491', '2bb31a0b-2332-48ec-8676-2331e2f9cad0',
                              '3bd597dd-95ec-4b6a-b7f1-7b2370c65ca3', '443fde7d-5958-45c1-9d97-70368e5769e4', '685d2ab6-221c-4659-b146-5e240fa22a8e',
                              '990b80e3-1e90-48f0-a78f-8871580f7a09', '9a849d45-5b6e-417f-8e49-08ea9d4e75b9', 'b939a070-af06-4831-9727-14421c269a10',
                              'c97af7f6-8d36-4674-8d6e-18a7023cfef8', 'cfe4d9bc-6790-4268-802a-47f48a3904cc', 'e5dc6302-5f16-4c71-a282-ecf93393efaa',
                              'f54d011e-7d27-4b9d-9b83-211d532d84e3', 'fbc30a1e-4a39-436c-bc94-44fd2452d54e']
            counter = 0
            for mountain in user_mountains:
                if str(mountain.mountain_id) in below_thousand:
                    counter += 1   
            if counter == len(below_thousand):
                achievements_to_add.append(models.Users_Achievements(user_id=user_id, achievement_id=ach.achievement_id))                   
                     
    db.add_all(achievements_to_add)
    db.commit()
    return {"status": "success"}