from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Posts']
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User =  Depends(oauth2.get_current_user) ):
    
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} is not Found!!!")
   
        
    vote_query =  db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    
    if(vote.dir == 1):
        if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" user of id :{current_user.id} already like this vote {vote.post_id}") 
        
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "success"}
    
    else:
        if not found_vote :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote_does_note_exists") 
        
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "vote deleted"}