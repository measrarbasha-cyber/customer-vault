import sqlite3
import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Verified Real Contact Enrichment Dictionary
VERIFIED_CONTACTS = {
    6: {
        "contact_info": "+91 98202 22028 | 022-6654 8178 | miten@bellwethercapital.in | MD, Bellwether Capital, 508 Raheja Chambers, Nariman Point, Mumbai"
    },
    7: {
        "contact_info": "+91 94263 11101 | 079-26650339 | drsanjeev@hvl.co.in | Director, Vijayratna Diabetes Centre, Paldi, Ahmedabad"
    },
    12: {
        "contact_info": "022-6133 4400 (Lodha Group Executive Desk) | Sanjiv Walke (Designated Person) / Ramkant Walke | Sakinaka, Mumbai"
    },
    19: {
        "contact_info": "+91 99250 79009 | 0285-2628301 | Dr. M. V. Pansuriya, Pansuriya Nidan Kendra, Balaji Ave, Moti Baug, Junagadh"
    },
    20: {
        "contact_info": "+91 80-45007854 | kavish@stones2milestones.com | go@getfreadom.com | Founder/CEO, Stones2Milestones, Gurgaon"
    },
    21: {
        "contact_info": "+91 7942703516 | 0651-2311929 | 0651-2900797 | Sanitary Sales Corp (Astral Distributor), Narsaria Tower, Lalpur, Ranchi"
    },
    22: {
        "contact_info": "+1 (936) 876-5719 | Fax: +1 (936) 876-3308 | Dr. Lenin Pinnamaneni, MD, Woodland Heights Medical Center, Huntington, TX, USA"
    },
    23: {
        "contact_info": "+91 98260 82720 | +91 98260 82725 | shyambhatia@rediffmail.com | cashyambhatia.com | Shyam Bhatia & Co., CAs, Indore"
    },
    24: {
        "contact_info": "+91 98997 07670 | ca.loveseema@gmail.com | Official ICAI Registry | G-707 Rashmi Apts, Pitampura, Delhi"
    },
    26: {
        "contact_info": "079-22148303 (Direct Store Desk) | Central Watch Co., 3116 Gandhi Road, Near Chandra Vilas Hotel, Ahmedabad"
    },
    27: {
        "contact_info": "+91 94895 31976 | Cheese Corner / Rotary Club Metro | Jyothi Illam, Vallabai Road, Chokkikulam, Madurai"
    },
    30: {
        "contact_info": "+91 86575 88506 | +91 88661 06565 | 02692-222424 | destinationhonda@gmail.com | Director, Destination Motors / Downtown Auto, Karamsad, Anand"
    },
    31: {
        "contact_info": "+91 79038 69075 | +91 80477 97559 | Rampuria Garments / Cloth Stores, Tulsi Chowk, Doranda Bazar, Ranchi"
    },
    32: {
        "contact_info": "+91 94260 14576 | +91 99789 14576 | prakashtekwani@yahoo.com | Prakash Tekwani & Associates (CAs), Karnavati Plaza, Revdi Bazar, Ahmedabad"
    },
    33: {
        "contact_info": "+91 97170 35556 | +91 95999 49945 | Max Super Speciality Hospital, Shalimar Bagh / Vaishali, Pitampura, Delhi"
    },
    34: {
        "contact_info": "079-26420166 | 079-68198992 | info@madhuvan.com | ashish@madhuvan.com | Madhuram Traders / Madhuvan, Ellisbridge, Ahmedabad"
    },
    35: {
        "contact_info": "+91 94222 35934 | +91 94227 12637 | 1800-267-4987 | contact@endoworldhospital.com | Endoworld Hospital, Jalna Rd, Aurangabad"
    },
    36: {
        "contact_info": "0231-2667342 | 0231-2667344 | export@priyabags.com | priyadarshini_polysacks@yahoo.com | Corporate Office, Priyadarshini Polysacks, Kolhapur"
    },
    37: {
        "contact_info": "+91 87329 51452 | 02673-242927 | Gandhi Children Hospital, Dolatgang Bazar, Dahod, Gujarat"
    },
    38: {
        "contact_info": "07152-240280 | +91 9823022110 | +91 8888993818 | Netra Eye Hospital, Ingole Chowk, Arvi Road, Wardha"
    },
    40: {
        "contact_info": "022-4006 2982 | pn@sfplcorp.com | Dipak Agarwalla HUF, Saurashtra Fuels Pvt Ltd, 93 C Mittal Tower, Nariman Point, Mumbai"
    },
    44: {
        "contact_info": "+91 98110 23415 | +91 98737 23415 | Parul Gupta & Vishal Kumar Gupta | 48 Banarsi Dass Estate, Timarpur, Delhi"
    },
    46: {
        "contact_info": "022-6654 8178 | norma@bellwethercapital.in | ranjit@bellwethercapital.in | Bellwether Capital, 508 Raheja Chambers, Nariman Point, Mumbai"
    },
    67: {
        "contact_info": "+91 98916 67799 | krishnan@adroitoptions.com | Director, JP Adroit Consultants, Elita Promenade, JP Nagar 7th Phase, Bangalore"
    },
    78: {
        "contact_info": "011-45537559 | +91 89208 31225 | premierpoly@premierpoly.com | Promoter Group, Premier Polyfilm Ltd, Vrindavan Farm, Vasant Kunj, Delhi"
    }
}

def update_db(db_path):
    print(f"Updating database: {db_path}")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    count = 0
    for cid, info in VERIFIED_CONTACTS.items():
        c.execute("UPDATE customers SET contact_info = ? WHERE id = ?", (info["contact_info"], cid))
        if c.rowcount > 0:
            count += 1
    conn.commit()
    conn.close()
    print(f"  Successfully updated {count} records in {db_path}.")

def main():
    update_db("customers.db")
    update_db("uploads/customers.db")
    
    # Sync candidate json if present
    try:
        with open("enrichment_candidates.json", "r", encoding="utf-8") as f:
            candidates = json.load(f)
        for cand in candidates:
            if cand["id"] in VERIFIED_CONTACTS:
                cand["contact_info"] = VERIFIED_CONTACTS[cand["id"]]["contact_info"]
        with open("enrichment_candidates.json", "w", encoding="utf-8") as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
        print("Updated enrichment_candidates.json")
    except Exception as e:
        print(f"Could not update candidates json: {e}")

if __name__ == "__main__":
    main()
