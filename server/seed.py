from app import app, db, User, Pet, PetStore, Review
from faker import Faker
import random

fake = Faker()

speciesArray = ["Dog", "Cat", "Fish", "Bird", "Hamster", "Reptile"]

# Array of comments related to reviewing a pet store
review_comments = [
    "Great selection of pets!",
    "Friendly staff and clean environment.",
    "The prices are reasonable.",
    "I love the variety of species they have.",
    "The store is well-maintained and organized.",
    "Excellent customer service.",
    "The pet store is my go-to place for all pet supplies.",
    "I highly recommend this pet store.",
    "They have unique and rare species.",
    "Knowledgeable staff members.",
    "The pet store has a welcoming atmosphere.",
    "My pets always enjoy their purchases from here.",
    "The staff goes above and beyond to assist customers.",
    "The pet store supports local animal shelters.",
    "Fair and transparent pricing.",
    "A great place for pet enthusiasts!",
    "Clean and spacious store layout.",
    "I found everything I needed for my furry friends.",
    "The pet store hosts informative events for pet owners.",
    "The pet store contributes to community events.",
]



def seed_data():
    with app.app_context():
        
        print('<<<<<<=Deleting existing seed data=>>>>>>')
        User.query.delete()
        Pet.query.delete()
        PetStore.query.delete()
        Review.query.delete()
        
        db.create_all()
        
        print('<<<<<<=Seeding new data to the tables=>>>>>>')
        
        # Users data
        users = []
        for _ in range(10):
            user = User(username=fake.name(),
                        email=fake.email(),
                        phone_number=fake.random_int(min=1000000000, max=9999999999),
                        password=fake.password(),
                        )
            users.append(user)
            db.session.add(user)
        db.session.commit()
        
        # Pet Stores data
        pet_stores = []
        for _ in range(5):
            pet_store = PetStore(name=fake.company(),
                                 location=fake.address(),
                                 phone_number=fake.random_int(min=1000000000, max=9999999999),
                                 email=fake.company_email(),
                                 )
            pet_stores.append(pet_store)
            db.session.add(pet_store)
        db.session.commit()
        
        # Pets data
        pets = []
        for _ in range(20):
            user = random.choice(users)
            pet_store = random.choice(pet_stores)
            
            pet = Pet(name=fake.first_name(),
                      species=random.choice(speciesArray),
                      price=random.randint(10, 100),
                      age=random.randint(1, 10),
                      user=user,
                      pet_store=pet_store,
                      )
            pets.append(pet)
            db.session.add(pet)
        db.session.commit()
        
        # Reviews data
        reviews = []
        for _ in range(15):
            user = random.choice(users)
            pet_store = random.choice(pet_stores)
            
            review = Review(Rating=fake.random_int(min=1, max=5),
                            Comments=random.choice(review_comments),
                            user=user,
                            pet_store=pet_store,
                            )
            reviews.append(review)
            db.session.add(review)
        db.session.commit()
        
        print('<<<<<<= Completed seeding! =>>>>>>')

if __name__ == '__main__':
    seed_data()