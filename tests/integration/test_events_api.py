from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.storage.storage import events



client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_memory():
    events.clear()

def test_create_event_api_success():
    response = client.post("/event", data = 
        {
            "title": "Reunion",
            "description": "Meeting old school mates",
            "date": "02-03-2026",
            "location": "Enugu"
        },
        files = {
            "flyer": ("good_pic.png", b"picturecontent", "image/png")
        }
    )
    
    assert response.status_code == 201
    
    data = response.json()
    
    assert data == {
        "id": 1,
        "title": "Reunion",
        "description": "Meeting old school mates",
        "date": "02-03-2026",
        "location": "Enugu",
        "flyer": data["flyer"]
    }
    
    assert data["flyer"] is not None
    assert data["flyer"].endswith(".png")
    
    

def test_create_event_api_without_flyer():
    response = client.post("/event", data = 
        {
            "title": "Reunion",
            "description": "Meeting old school mates",
            "date": "02-03-2026",
            "location": "Enugu"
        }
    )   
    
    assert response.status_code == 201
    
    data = response.json()
    
    assert data == {
        "id": 1,
        "title": "Reunion",
        "description": "Meeting old school mates",
        "date": "02-03-2026",
        "location": "Enugu",
        "flyer": None
    }
    
    
    
def test_create_event_unsupported_media():
    response = client.post("/event", data = 
        {
            "title": "Bazzar",
            "description": "Church event",
            "date": "03-04-2026",
            "location": "Abia"
        },
        files= {
            "flyer": ("pic.txt", b"piccontent", "text/plain")
        }
    ) 
    
    assert response.status_code == 415   
    
    
    
    

def test_create_event_UnprocessableContentError():
    response = client.post("/event", data = 
        {
            "title": "",
            "description": "Church event",
            "date": "03-04-2026",
            "location": "Abia"
        }
    )
    
    assert response.status_code == 422  
    
    
    
    

def test_list_events_empty():
     response = client.get("/event/")
     
     assert response.status_code == 200
     assert response.json() == [] 
     
     


def test_list_events_success():
    client.post("/event", data = 
        {
            "title": "Reunion",
            "description": "Meeting old school mates",
            "date": "02-03-2026",
            "location": "Enugu"
        }
    ) 
    
    
    client.post("/event", data = 
        {
            "title": "Reunion 2",
            "description": "Meeting old school mates 2",
            "date": "02-04-2026",
            "location": "Enugu state"
        }
    )
    
    response = client.get("/event/")
    
    assert response.status_code == 200
    
    data = response.json()
    
    assert isinstance(data,list)
    assert len(data) == 2
    
    
    
    assert data == [
        {
            "id": 1,
            "title": "Reunion",
            "description": "Meeting old school mates",
            "date": "02-03-2026",
            "location": "Enugu",
            "flyer": None
        },
        {
            "id": 2,
            "title": "Reunion 2",
            "description": "Meeting old school mates 2",
            "date": "02-04-2026",
            "location": "Enugu state",
            "flyer": None
        }
    ]