import datetime
import calendar

# --- Constants & Mappers ---

ENG_MONTHS = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

BAN_MONTHS_TRANS = [
    "জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", 
    "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"
]

WEEKDAYS_BAN = ["রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"] 
# Python calendar 0=Mon, 6=Sun. Need to adjust.
# My preferred mapping: 0=Sun, 1=Mon... for the grid.


BANGLA_MONTHS_BN = [
    "বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", 
    "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"
]

HIJRI_MONTHS_BN = [
    "মহররম", "সফর", "রবিউল আউয়াল", "রবিউস সানি", "জমাদিউল আউয়াল", "জমাদিউল সানি", 
    "রজব", "শাবান", "রমজান", "শাওয়াল", "জিলকদ", "জিলহজ্জ"
]

def to_bangla_num(n):
    return str(n).translate(str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯"))

# --- Calculation Logic ---

def get_bangla_date(date_obj):
    # Anchor: April 14, 2026 is 1 Boishakh 1433
    anchor = datetime.date(2026, 4, 14)
    
    # 1433 Structure (Standard)
    # Boi-Bha (5 * 31), Ash-Chai (7 * 30), Falgun 29/30
    # Since 2027 is Feb, and 2027 not leap, Falgun 1433 (Feb/Mar 2027) is 29.
    # But for 2026 calendar we only care mostly about 1432 end and 1433 start.
    
    delta = (date_obj - anchor).days
    
    if delta >= 0:
        # Date is in 1433 (or later)
        year = 1433
        # Month lengths for 1433
        # 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29, 30? Wait.
        # Revised calendar: 
        # Boi-Bha (5): 31
        # Ash-Cho (7): 30 EXCEPT Falgun
        # Falgun: 29 (30 if leap)
        # Year 1433 Falgun falls in 2027 (not leap). So 29.
        
        months_lengths = [31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29, 30]
        
        day_count = delta
        m_idx = 0
        while day_count >= months_lengths[m_idx]:
            day_count -= months_lengths[m_idx]
            m_idx += 1
        
        bd_day = day_count + 1
        # m_idx 0 = Boishakh
        return bd_day, m_idx, year
        
    else:
        # Date is in 1432
        # Work backwards from Anchor (1 Boishakh 1433)
        # Prev day: 30 Chaitra 1432.
        # 1432 structure:
        # Falgun 1432 was in Feb/Mar 2026. 2026 not leap. Falgun 1432 = 29 days.
        # Chaitra 1432 = 30 days.
        # Magh 1432 = 30 days.
        # Poush 1432 = 30 days.
        
        # We need full structure of 1432 to be safe, or just reverse map.
        # Let's define 1432 end months lengths in reverse order from Chaitra.
        # Chaitra (idx 11), Falgun (idx 10), Magh (9), Poush (8) ...
        
        rev_lengths = [30, 29, 30, 30, 30, 30] # Chaitra, Falgun, Magh, Poush, Ogrohayon, Kartik
        # We only go back to Jan 1.
        # Jan 1 to Apr 13 is ~103 days.
        
        day_diff = -delta # Positive number of days before Apr 14
        # Day 1 before = Chaitra 30.
        
        # Logic: 
        # remaining = day_diff
        # iterates backwards through months
        
        curr_m_idx = 11 # Chaitra
        year = 1432
        
        # Special check for Falgun 1432 length
        # Falgun 2026 falls in Feb-Mar 2026. Not leap. 29 days.
        
        lengths_1432 = {11: 30, 10: 29, 9: 30, 8: 30, 7: 30, 6: 30} # enough for start of year
        
        while True:
            l = lengths_1432[curr_m_idx]
            if day_diff <= l:
                bd_day = l - day_diff + 1
                return bd_day, curr_m_idx, year
            day_diff -= l
            curr_m_idx -= 1

def get_hijri_date(date_obj):
    # Anchor: June 17, 2026 = 1 Muharram 1448
    anchor = datetime.date(2026, 6, 17)
    delta = (date_obj - anchor).days
    
    if delta >= 0:
        # 1448
        year = 1448
        # Standard tabular: 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29
        # Year 1448 is 8th year of cycle -> Not leap -> Dhu al-Hijjah 29.
        months_lengths = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29]
        
        day_count = delta
        m_idx = 0
        while m_idx < 12 and day_count >= months_lengths[m_idx]:
            day_count -= months_lengths[m_idx]
            m_idx += 1
            
        return day_count + 1, m_idx, year
    else:
        # 1447
        year = 1447
        # Work backwards from 1 Muharram 1448
        # Prev month: Dhu al-Hijjah 1447.
        # 1447 is leap (7th year). Dhu al-Hijjah is 30.
        # Order reverse: Dhu al-Hijjah, Dhu al-Qi'dah, ...
        # Normal lengths: 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29 (Muh..Hij)
        # Reversed: Hij(29/30), Qi(30), Shaw(29), Ram(30)...
        
        # 1447 lengths (Leap):
        # Muh(30), Saf(29), R1(30), R2(29), J1(30), J2(29), Raj(30), Sha(29), Ram(30), Shaw(29), Qi(30), Hij(30!)
        
        months_lengths_1447 = [30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30]
        
        day_diff = -delta # Days before 1448
        curr_m_idx = 11 # Dhu al-Hijjah
        
        while True:
            l = months_lengths_1447[curr_m_idx]
            if day_diff <= l:
                day = l - day_diff + 1
                return day, curr_m_idx, year
            day_diff -= l
            curr_m_idx -= 1

# --- HTML Generator ---

def generate_html():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>2026 Calendar</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+Bengali:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --color-gregorian: #000000;
            --color-bangla: #1a9e36; /* Green */
            --color-hijri: #004085; /* Darker Blue for contrast */
            --color-weekend: #dc2626; /* Red */
            --color-border: #d1d5db;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            font-family: 'Inter', sans-serif;
            background: white;
            max-width: 210mm;
            height: auto;
            min-height: 297mm;
            margin: 0 auto;
            padding: 8mm; 
            color: #111;
        }

        .header {
            text-align: center;
            margin-bottom: 5px; 
            border-bottom: 1px solid #ccc;
            padding-bottom: 4px;
        }
        .header h1 {
            font-family: 'Noto Sans Bengali', sans-serif;
            font-size: 22px; 
            font-weight: 700;
            margin-bottom: 2px;
            color: #333;
        }
        .header .subtext {
            font-family: 'Noto Sans Bengali', sans-serif;
            font-size: 11px;
            color: #555;
            display: flex;
            justify-content: center;
            gap: 15px;
            font-weight: 500;
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(4, 1fr);
            gap: 6px; 
            height: auto; 
        }

        .month-card {
            border: 1px solid var(--color-border);
            padding: 2px;
            display: flex;
            flex-direction: column;
            page-break-inside: avoid; /* Prevent splitting */
        }

        .month-header {
            text-align: center;
            margin-bottom: 2px;
            background: #f9fafb;
            padding: 2px 0;
            border-bottom: 1px solid #eee;
        }
        .month-name-bn {
            font-family: 'Noto Sans Bengali', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #111;
            line-height: 1.1;
        }
        .month-name-en {
            font-size: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #666;
            margin-top: -2px;
        }
        .sub-month-info {
            font-family: 'Noto Sans Bengali', sans-serif;
            font-size: 8px;
            color: #555;
            margin-top: 1px;
            display: flex;
            flex-direction: column;
            gap: 0px;
        }
        .sub-month-row {
            display: flex;
            justify-content: center;
            gap: 4px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
            flex-grow: 1;
        }
        
        th {
            font-family: 'Noto Sans Bengali', sans-serif;
            font-weight: 600;
            color: #444;
            border-bottom: 1px solid var(--color-border);
            padding: 1px 0;
            font-size: 10px;
        }
        th.weekend { color: var(--color-weekend); }

        td {
            height: 100%;
            vertical-align: top;
            border: 1px solid #f0f0f0;
            padding: 1px 2px;
            position: relative;
            height: 28px; 
        }
        
        /* Date Cell Layout */
        .date-cell {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
        }
        
        .gregorian {
            font-size: 13px;
            font-weight: 700;
            color: var(--color-gregorian);
            line-height: 0.9;
        }
        
        .secondary-dates {
            display: flex;
            justify-content: space-between;
            font-size: 8px;
            margin-top: 0px;
            align-items: flex-end;
        }
        
        .bangla-date { 
            color: var(--color-bangla); 
            font-family: 'Noto Sans Bengali', sans-serif; 
            font-weight: 600; 
            font-size: 9px;
        }
        .hijri-date { 
            color: var(--color-hijri); 
            font-family: 'Inter', sans-serif; 
            font-weight: 500;
            font-size: 8px;
        }

        .weekend-text .gregorian { color: var(--color-weekend); }
        .weekend-bg { background-color: #fef2f2; }

        @media print {
            body { 
                padding: 0; 
                margin: 10mm;
                -webkit-print-color-adjust: exact; 
                print-color-adjust: exact;
            }
            @page {
                size: A4 portrait;
                margin: 0;
            }
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>২০২৬ সালের ক্যালেন্ডার</h1>
        <div class="subtext">
            <span>বাংলা সন ১৪৩২–১৪৩৩</span>
            <span>•</span>
            <span>হিজরি সন ১৪৪৭–১৪৪৮</span>
        </div>
    </div>

    <div class="calendar-grid">
"""

    # Generate each month
    for m in range(1, 13):
        # Month Header
        bn_name = BAN_MONTHS_TRANS[m-1]
        en_name = ENG_MONTHS[m-1]
        
        # Calculate start and end months for Bangla and Hijri
        start_date = datetime.date(2026, m, 1)
        _, days_in_month = calendar.monthrange(2026, m)
        end_date = datetime.date(2026, m, days_in_month)
        
        # Bangla Range
        _, bd_m_start, bd_y_start = get_bangla_date(start_date)
        _, bd_m_end, bd_y_end = get_bangla_date(end_date)
        
        bd_str = ""
        if bd_m_start == bd_m_end:
             bd_str = f"{BANGLA_MONTHS_BN[bd_m_start]} {to_bangla_num(bd_y_start)}"
        else:
             if bd_y_start == bd_y_end:
                 bd_str = f"{BANGLA_MONTHS_BN[bd_m_start]}-{BANGLA_MONTHS_BN[bd_m_end]} {to_bangla_num(bd_y_start)}"
             else:
                 bd_str = f"{BANGLA_MONTHS_BN[bd_m_start]} {to_bangla_num(bd_y_start)} - {BANGLA_MONTHS_BN[bd_m_end]} {to_bangla_num(bd_y_end)}"
                 
        # Hijri Range
        _, hj_m_start, hj_y_start = get_hijri_date(start_date)
        _, hj_m_end, hj_y_end = get_hijri_date(end_date)
        
        hj_str = ""
        if hj_m_start == hj_m_end:
            hj_str = f"{HIJRI_MONTHS_BN[hj_m_start]} {to_bangla_num(hj_y_start)}"
        else:
            if hj_y_start == hj_y_end:
                hj_str = f"{HIJRI_MONTHS_BN[hj_m_start]}-{HIJRI_MONTHS_BN[hj_m_end]} {to_bangla_num(hj_y_start)}"
            else:
                 hj_str = f"{HIJRI_MONTHS_BN[hj_m_start]} {to_bangla_num(hj_y_start)} - {HIJRI_MONTHS_BN[hj_m_end]} {to_bangla_num(hj_y_end)}"

        html += f"""
        <div class="month-card">
            <div class="month-header">
                <div class="month-name-bn">{bn_name}</div>
                <div class="month-name-en">{en_name}</div>
                <div class="sub-month-info">
                   <div class="sub-month-row" style="color: var(--color-bangla);">{bd_str}</div>
                   <div class="sub-month-row" style="color: var(--color-hijri);">{hj_str}</div>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>রবি</th>
                        <th>সোম</th>
                        <th>মঙ্গল</th>
                        <th>বুধ</th>
                        <th>বৃহঃ</th>
                        <th class="weekend">শুক্র</th>
                        <th class="weekend">শনি</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Calendar matrix
        # monthrange returns (weekday_of_first, days_in_month)
        # python weekday: 0=Mon, ... 6=Sun.
        # we want 0=Sun. 
        # python: Mon(0), Tue(1), Wed(2), Thu(3), Fri(4), Sat(5), Sun(6)
        # target: Sun(0), Mon(1)...
        # So target_wd = (python_wd + 1) % 7
        
        first_wd, days_in_month = calendar.monthrange(2026, m)
        start_col = (first_wd + 1) % 7
        
        current_day = 1
        
        # Grid is 6 rows max usually
        for row in range(6):
            if current_day > days_in_month: break
            
            html += "<tr>"
            for col in range(7):
                if (row == 0 and col < start_col) or current_day > days_in_month:
                    html += "<td></td>"
                else:
                    date_obj = datetime.date(2026, m, current_day)
                    
                    # Convert dates
                    bd_day, bd_m, bd_y = get_bangla_date(date_obj)
                    hj_day, hj_m, hj_y = get_hijri_date(date_obj)
                    
                    is_weekend = (col == 0 or col == 5 or col == 6) # Sun(0), Fri(5), Sat(6)
                    # User asked for Fri & Sat RED. Sun starts week.
                    # Wait, is Sunday red? "Friday highlighted in RED, Saturday highlighted in RED".
                    # Usually in BD, Fri/Sat are holidays.
                    # My class logic: Sun=0. Fri=5, Sat=6.
                    
                    weekend_class = "weekend-text" if (col == 5 or col == 6) else ""
                    # cell_bg = "weekend-bg" if (col == 5 or col == 6) else "" 
                    # keep white bg for cleanliness, just red text
                    
                    bd_str = to_bangla_num(bd_day)
                    
                    html += f"""
                    <td class="{weekend_class}">
                        <div class="date-cell">
                            <div class="gregorian">{current_day}</div>
                            <div class="secondary-dates">
                                <span class="bangla-date">{bd_str}</span>
                                <span class="hijri-date">{hj_day}</span>
                            </div>
                        </div>
                    </td>
                    """
                    current_day += 1
            html += "</tr>"
            
        html += """
                </tbody>
            </table>
        </div>
        """
        
    html += """
    </div>
</body>
</html>
"""
    return html

if __name__ == '__main__':
    content = generate_html()
    with open('calendar_2026.html', 'w', encoding='utf-8') as f:
        f.write(content)
