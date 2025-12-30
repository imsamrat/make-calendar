import csv
import datetime
import calendar

# --- Constants ---
ENG_MONTHS = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

BAN_MONTHS_TRANS = [
    "জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", 
    "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"
]

BANGLA_MONTHS_BN = [
    "বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", 
    "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"
]

HIJRI_MONTHS_BN = [
    "মহররম", "সফর", "রবিউল আউয়াল", "রবিউস সানি", "জমাদিউল আউয়াল", "জমাদিউল সানি", 
    "রজব", "শাবান", "রমজান", "শাওয়াল", "জিলকদ", "জিলহজ্জ"
]

WEEKDAYS_BN = ["রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"]

def to_bangla_num(n):
    return str(n).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))

# --- Calculation Logic (Same as before) ---
def get_bangla_date(date_obj):
    anchor = datetime.date(2026, 4, 14)
    delta = (date_obj - anchor).days
    
    if delta >= 0:
        year = 1433
        months_lengths = [31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29, 30]
        day_count = delta
        m_idx = 0
        while day_count >= months_lengths[m_idx]:
            day_count -= months_lengths[m_idx]
            m_idx += 1
        return day_count + 1, m_idx, year
    else:
        day_diff = -delta
        rev_lengths = [30, 29, 30, 30, 30, 30] 
        lengths_1432 = {11: 30, 10: 29, 9: 30, 8: 30, 7: 30, 6: 30}
        curr_m_idx = 11 
        year = 1432
        while True:
            l = lengths_1432[curr_m_idx]
            if day_diff <= l:
                bd_day = l - day_diff + 1
                return bd_day, curr_m_idx, year
            day_diff -= l
            curr_m_idx -= 1

def get_hijri_date(date_obj):
    anchor = datetime.date(2026, 6, 17)
    delta = (date_obj - anchor).days
    if delta >= 0:
        year = 1448
        months_lengths = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        day_count = delta
        m_idx = 0
        while m_idx < 12 and day_count >= months_lengths[m_idx]:
            day_count -= months_lengths[m_idx]
            m_idx += 1
        return day_count + 1, m_idx, year
    else:
        year = 1447
        months_lengths_1447 = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30]
        day_diff = -delta
        curr_m_idx = 11
        while True:
            l = months_lengths_1447[curr_m_idx]
            if day_diff <= l:
                day = l - day_diff + 1
                return day, curr_m_idx, year
            day_diff -= l
            curr_m_idx -= 1

# --- CSV Generation ---
def generate_csv():
    rows = []
    # Header row
    header = ["Gregorian Month", "Bangla Month Name", "Date", "Day Name", "Bangla Date", "Hijri Date", "Bangla Month Full", "Hijri Month Full"]
    rows.append(header)

    for m in range(1, 13):
        days_in_month = calendar.monthrange(2026, m)[1]
        for d in range(1, days_in_month + 1):
            date_obj = datetime.date(2026, m, d)
            
            # Info
            en_month = ENG_MONTHS[m-1]
            bn_trans_month = BAN_MONTHS_TRANS[m-1]
            day_name = WEEKDAYS_BN[(date_obj.weekday() + 1) % 7]
            
            # Dates
            bd_d, bd_m, bd_y = get_bangla_date(date_obj)
            hj_d, hj_m, hj_y = get_hijri_date(date_obj)
            
            row = [
                en_month,
                bn_trans_month,
                d,
                day_name,
                to_bangla_num(bd_d),
                hj_d,
                f"{BANGLA_MONTHS_BN[bd_m]} {to_bangla_num(bd_y)}",
                f"{HIJRI_MONTHS_BN[hj_m]} {to_bangla_num(hj_y)}"
            ]
            rows.append(row)

    with open('calendar_2026_data.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

if __name__ == '__main__':
    generate_csv()
