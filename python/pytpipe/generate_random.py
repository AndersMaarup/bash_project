import os
import random

first_name_list = [
    "John", "Jane", "Alex", "Emily", "Chris", "Katie", "Michael", "Sarah", "David", "Laura", 
    "James", "Hannah", "Robert", "Jessica", "Daniel", "Samantha", "William", "Megan", "Joseph", "Rachel", 
    "Thomas", "Rebecca", "Charles", "Amanda", "Matthew", "Ashley", "Anthony", "Brittany", "Mark", "Jennifer", 
    "Paul", "Melissa", "Steven", "Nicole", "Andrew", "Stephanie", "Joshua", "Amber", "Brian", "Katherine", 
    "Kevin", "Victoria", "Jason", "Natalie", "Eric", "Alyssa", "Timothy", "Morgan", "Ryan", "Brooke", 
    "Jacob", "Caitlin", "Nicholas", "Madison", "Jonathan", "Haley", "Adam", "Allison", "Richard", "Kayla", 
    "Jeffrey", "Sophia", "Scott", "Isabella", "Benjamin", "Olivia", "Justin", "Emma", "Brandon", "Chloe", 
    "Samuel", "Ella", "Gregory", "Ava", "Patrick", "Mia", "Stephen", "Abigail", "Kenneth", "Grace", 
    "Ronald", "Zoe", "Edward", "Lily", "George", "Frank", "Larry", "Ariana", "Jerry", "Stella", 
    "Henry", "Violet", "Carl", "Lillian", "Arthur", "Nora", "Walter", "Hazel"
]

last_name_list = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez"
]

corporation_list = [
    "TechSolutions Inc.", "GreenEnergy Corp.", "Skyline Ventures", "Pinnacle Holdings", "Apex Innovations", 
    "Summit Enterprises", "Quantum Dynamics", "FusionTech Systems", "Evergreen Industries", "GlobalTrade Ltd.", 
    "CrystalClear Technologies", "BlueWave Networks", "NextGen Solutions", "FutureProof LLC", "OmniSource Corp.", 
    "InfiniteLoop Ltd.", "PrimeLogistics", "Visionary Labs", "BrightPath Services", "SolarFlare Innovations", 
    "Hyperion Industries", "Vertex Pharmaceuticals", "AlphaOmega Inc.", "Zenith Technologies", "Galaxy Enterprises", 
    "StarLink Solutions", "Ascend Financial", "Insight Analytics", "EcoWise Corp.", "UrbanGrid Systems", 
    "AstraNova Inc.", "Pioneer Ventures", "Fortress Security", "AquaPure Technologies", "Synergy Innovations", 
    "TransGlobal Inc.", "Vertex Logistics", "Nexus Solutions", "EnviroGuard Systems", "Titan Enterprises", 
    "Neptune Networks", "Frontier Solutions", "TerraTech Industries", "Optima Services", "MagnaTech Systems", 
    "CoreVision Inc.", "Pulse Innovations", "Vanguard Holdings", "Revolutionary Solutions", "Catalyst Enterprises", 
    "NovaTech Corp.", "Everest Holdings", "FusionWave Technologies", "GlobalReach Ltd.", "Epicenter Solutions", 
    "ProActive Ventures", "BrightFuture Inc.", "OmegaWave Technologies", "NexGen Industries", "Elemental Systems", 
    "Aspire Solutions", "Beacon Technologies", "Solaris Innovations", "TerraFirma Corp.", "ProTech Services", 
    "EagleEye Systems", "Pathfinder Ventures", "OptiMax Solutions", "QuantumLeap Inc.", "Noble Enterprises", 
    "Radiant Technologies", "Innovatech Solutions", "Prime Innovations", "EcoLogic Systems", "Helix Corp.", 
    "Precision Dynamics", "Epic Innovations", "AdvancedTech Corp.", "Frontline Solutions", "Superior Services", 
    "SkyHigh Innovations", "BrightMind Systems", "EnviroSafe Inc.", "Triumph Holdings", "NextWave Technologies", 
    "Vertex Innovations", "GreenTech Industries", "SynergyTech Solutions", "QuantumEdge Corp.", "Visionary Enterprises", 
    "EcoFuture Systems", "ProLogic Solutions", "AeroTech Inc.", "CoreTech Innovations", "Optimal Solutions", 
    "PrimeTech Corp.", "BrightVision Ltd.", "Infinity Solutions", "Alpha Industries", "GlobalTech Systems"
]

def generate_list(length):
    data = []
    for _ in range(length):
        first_name = random.choice(first_name_list)
        last_name = random.choice(last_name_list)
        phonenumber = f"{random.randint(100, 999)}-555-{random.randint(1000, 9999)}"
        corporation = random.choice(corporation_list)
        data.append(f"{first_name}, {last_name}, {phonenumber}, {corporation}, {phonenumber}")
    
    # Make file path
    file_path = os.path.join("./test", "clientList.txt")
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Open file and write each entry on a new line
    with open(file_path, "w") as file:
        for line in data:
            file.write(line + "\n")
    
    return file_path