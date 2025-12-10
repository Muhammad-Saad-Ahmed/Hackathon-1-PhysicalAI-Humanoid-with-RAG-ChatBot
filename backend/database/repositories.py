from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.textbook import Textbook, TextbookCreate, TextbookUpdate
from ..models.chapter import Chapter, ChapterCreate, ChapterUpdate
from ..models.section import Section, SectionCreate, SectionUpdate
from ..models.generation_params import GenerationParameter, GenerationParameterCreate, SavedGenerationParameterSetCreate, SavedGenerationParameterSetUpdate
from ..models.chat_session import ChatSession, ChatSessionCreate
from ..models.chat_message import ChatMessage, ChatMessageCreate
from ..database.database import Base, SavedGenerationParameterSet


class TextbookRepository:
    @staticmethod
    def create(db: Session, textbook: TextbookCreate) -> Textbook:
        db_textbook = Textbook(**textbook.dict())
        db.add(db_textbook)
        db.commit()
        db.refresh(db_textbook)
        return db_textbook

    @staticmethod
    def get(db: Session, textbook_id: str) -> Optional[Textbook]:
        return db.query(Textbook).filter(Textbook.id == textbook_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Textbook]:
        return db.query(Textbook).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, textbook_id: str, textbook_update: TextbookUpdate) -> Optional[Textbook]:
        db_textbook = db.query(Textbook).filter(Textbook.id == textbook_id).first()
        if db_textbook:
            for field, value in textbook_update.dict(exclude_unset=True).items():
                setattr(db_textbook, field, value)
            db.commit()
            db.refresh(db_textbook)
        return db_textbook

    @staticmethod
    def delete(db: Session, textbook_id: str) -> bool:
        db_textbook = db.query(Textbook).filter(Textbook.id == textbook_id).first()
        if db_textbook:
            db.delete(db_textbook)
            db.commit()
            return True
        return False


class ChapterRepository:
    @staticmethod
    def create(db: Session, chapter: ChapterCreate) -> Chapter:
        db_chapter = Chapter(**chapter.dict())
        db.add(db_chapter)
        db.commit()
        db.refresh(db_chapter)
        return db_chapter

    @staticmethod
    def get(db: Session, chapter_id: str) -> Optional[Chapter]:
        return db.query(Chapter).filter(Chapter.id == chapter_id).first()

    @staticmethod
    def get_by_textbook(db: Session, textbook_id: str) -> List[Chapter]:
        return db.query(Chapter).filter(Chapter.textbook_id == textbook_id).order_by(Chapter.position).all()

    @staticmethod
    def update(db: Session, chapter_id: str, chapter_update: ChapterUpdate) -> Optional[Chapter]:
        db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if db_chapter:
            for field, value in chapter_update.dict(exclude_unset=True).items():
                setattr(db_chapter, field, value)
            db.commit()
            db.refresh(db_chapter)
        return db_chapter

    @staticmethod
    def delete(db: Session, chapter_id: str) -> bool:
        db_chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if db_chapter:
            db.delete(db_chapter)
            db.commit()
            return True
        return False


class SectionRepository:
    @staticmethod
    def create(db: Session, section: SectionCreate) -> Section:
        db_section = Section(**section.dict())
        db.add(db_section)
        db.commit()
        db.refresh(db_section)
        return db_section

    @staticmethod
    def get(db: Session, section_id: str) -> Optional[Section]:
        return db.query(Section).filter(Section.id == section_id).first()

    @staticmethod
    def get_by_chapter(db: Session, chapter_id: str) -> List[Section]:
        return db.query(Section).filter(Section.chapter_id == chapter_id).order_by(Section.position).all()

    @staticmethod
    def update(db: Session, section_id: str, section_update: SectionUpdate) -> Optional[Section]:
        db_section = db.query(Section).filter(Section.id == section_id).first()
        if db_section:
            for field, value in section_update.dict(exclude_unset=True).items():
                setattr(db_section, field, value)
            db.commit()
            db.refresh(db_section)
        return db_section

    @staticmethod
    def delete(db: Session, section_id: str) -> bool:
        db_section = db.query(Section).filter(Section.id == section_id).first()
        if db_section:
            db.delete(db_section)
            db.commit()
            return True
        return False


class GenerationParameterRepository:
    @staticmethod
    def create(db: Session, param: GenerationParameterCreate) -> GenerationParameter:
        db_param = GenerationParameter(**param.dict())
        db.add(db_param)
        db.commit()
        db.refresh(db_param)
        return db_param

    @staticmethod
    def get(db: Session, param_id: str) -> Optional[GenerationParameter]:
        return db.query(GenerationParameter).filter(GenerationParameter.id == param_id).first()

    @staticmethod
    def get_by_textbook(db: Session, textbook_id: str) -> List[GenerationParameter]:
        return db.query(GenerationParameter).filter(GenerationParameter.textbook_id == textbook_id).all()

    @staticmethod
    def delete(db: Session, param_id: str) -> bool:
        db_param = db.query(GenerationParameter).filter(GenerationParameter.id == param_id).first()
        if db_param:
            db.delete(db_param)
            db.commit()
            return True
        return False


class ChatSessionRepository:
    @staticmethod
    def create(db: Session, session: ChatSessionCreate) -> ChatSession:
        db_session = ChatSession(**session.dict())
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def get(db: Session, session_id: str) -> Optional[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.id == session_id).first()

    @staticmethod
    def get_by_textbook(db: Session, textbook_id: str) -> List[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.textbook_id == textbook_id).all()

    @staticmethod
    def delete(db: Session, session_id: str) -> bool:
        db_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
        if db_session:
            db.delete(db_session)
            db.commit()
            return True
        return False


class ChatMessageRepository:
    @staticmethod
    def create(db: Session, message: ChatMessageCreate) -> ChatMessage:
        db_message = ChatMessage(**message.dict())
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def get(db: Session, message_id: str) -> Optional[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.id == message_id).first()

    @staticmethod
    def get_by_session(db: Session, session_id: str) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).all()

    @staticmethod
    def delete(db: Session, message_id: str) -> bool:
        db_message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
        if db_message:
            db.delete(db_message)
            db.commit()
            return True
        return False


class SavedGenerationParameterSetRepository:
    @staticmethod
    def create(db: Session, saved_set: SavedGenerationParameterSetCreate) -> SavedGenerationParameterSet:
        db_saved_set = SavedGenerationParameterSet(**saved_set.dict())
        db.add(db_saved_set)
        db.commit()
        db.refresh(db_saved_set)
        return db_saved_set

    @staticmethod
    def get(db: Session, saved_set_id: str) -> Optional[SavedGenerationParameterSet]:
        return db.query(SavedGenerationParameterSet).filter(SavedGenerationParameterSet.id == saved_set_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[SavedGenerationParameterSet]:
        return db.query(SavedGenerationParameterSet).filter(SavedGenerationParameterSet.name == name).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[SavedGenerationParameterSet]:
        return db.query(SavedGenerationParameterSet).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, saved_set_id: str, saved_set_update: SavedGenerationParameterSetUpdate) -> Optional[SavedGenerationParameterSet]:
        db_saved_set = db.query(SavedGenerationParameterSet).filter(SavedGenerationParameterSet.id == saved_set_id).first()
        if db_saved_set:
            for field, value in saved_set_update.dict(exclude_unset=True).items():
                setattr(db_saved_set, field, value)
            db.commit()
            db.refresh(db_saved_set)
        return db_saved_set

    @staticmethod
    def delete(db: Session, saved_set_id: str) -> bool:
        db_saved_set = db.query(SavedGenerationParameterSet).filter(SavedGenerationParameterSet.id == saved_set_id).first()
        if db_saved_set:
            db.delete(db_saved_set)
            db.commit()
            return True
        return False