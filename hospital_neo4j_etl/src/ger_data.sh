#!/bin/bash

# Hospital Info File Generator for RAG System
# This script creates detailed hospital information files
# feel free to increase variety by turning more portions of the text into variables and inserting values from arrays of options.

# Arrays for randomized content
specialties=(
    "Cardiology" "Neurology" "Orthopedics" "Pediatrics" "Oncology" 
    "Emergency Medicine" "Internal Medicine" "Surgery" "Radiology" 
    "Psychiatry" "Dermatology" "Gastroenterology" "Pulmonology" 
    "Endocrinology" "Nephrology" "Rheumatology" "Ophthalmology"
    "Otolaryngology" "Urology" "Anesthesiology" "Pathology"
)

founding_years=("1967" "1972" "1985" "1991" "1998" "2003" "2008" "2015")
bed_counts=("150" "275" "320" "185" "410" "298" "163" "225" "350" "195")
emergency_locations=("West Wing, Ground Floor" "East Wing, Level 1" "Main Building, First Floor" "North Tower, Ground Level" "South Building, Entry Level")
parking_info=("Main parking garage with 500 spaces" "Surface parking lot with 200 spaces" "Multi-level parking structure" "Valet parking available" "Street parking and nearby garage")

# Hospital list
hospitals=(
    "Wallace-Hamilton" "Burke" "Griffin and Cooper" "Walton LLC" "Garcia Ltd"
    "Jones, Brown and Murray" "Boyd PLC" "Wheeler, Bryant and Johns" "Brown Inc"
    "Smith, Edwards and Obrien" "Brown-Golden" "Little-Spencer" "Rose Inc"
    "Malone, Thompson and Mejia" "Mcneil-Ali" "Jones, Taylor and Garcia"
    "Richardson-Powell" "Castaneda-Hardy" "Burch-White" "Cunningham and Sons"
    "Bell, Mcknight and Willis" "Pugh-Rogers" "Rush, Owens and Johnson"
    "Pearson LLC" "Taylor and Sons" "Schultz-Powers"
)

# Function to get random element from array
get_random() {
    local arr=("$@")
    echo "${arr[RANDOM % ${#arr[@]}]}"
}

# Function to get random specialties
get_random_specialties() {
    local count=$((RANDOM % 5 + 4))  # 4-8 specialties
    local selected=()
    local temp_specialties=("${specialties[@]}")
    
    for ((i=0; i<count; i++)); do
        local idx=$((RANDOM % ${#temp_specialties[@]}))
        selected+=("${temp_specialties[$idx]}")
        unset 'temp_specialties[$idx]'
        temp_specialties=("${temp_specialties[@]}")
    done
    
    printf "%s\n" "${selected[@]}"
}

# Function to create hospital file
create_hospital_file() {
    local hospital_name="$1"
    local filename="${hospital_name// /_}_Hospital_Info.txt"
    local founding_year=$(get_random "${founding_years[@]}")
    local beds=$(get_random "${bed_counts[@]}")
    local emergency_loc=$(get_random "${emergency_locations[@]}")
    local parking=$(get_random "${parking_info[@]}")
    
    cat > "$filename" << EOF
================================================================================
${hospital_name} MEDICAL CENTER - COMPREHENSIVE INFORMATION
================================================================================

ABOUT US
--------
${hospital_name} Medical Center has been serving our community since ${founding_year}, 
providing exceptional healthcare with a commitment to innovation, compassion, and 
clinical excellence. Our ${beds}-bed facility combines state-of-the-art medical 
technology with personalized patient care, making us a trusted healthcare partner 
for families throughout the region.

We pride ourselves on our multidisciplinary approach to healthcare, where our 
experienced medical professionals work collaboratively to ensure the best possible 
outcomes for every patient. Our mission is to deliver comprehensive, patient-centered 
care while advancing medical knowledge through research and education.

MEDICAL SPECIALTIES & SERVICES
------------------------------
Our hospital offers comprehensive medical services across multiple specialties:

$(get_random_specialties | sed 's/^/• /')

Each specialty department features board-certified physicians, advanced diagnostic 
equipment, and evidence-based treatment protocols. We maintain accreditation from 
relevant medical boards and participate in clinical trials to offer cutting-edge 
treatment options.

EMERGENCY DEPARTMENT ACCESS
---------------------------
LOCATION: ${emergency_loc}

FROM MAIN ENTRANCE:
1. Enter through the main lobby doors
2. Follow the RED emergency signs and floor markings
3. Take the elevator or stairs as directed by signage
4. The Emergency Department is clearly marked with large red "EMERGENCY" signs
5. If lost, ask any staff member wearing a hospital ID badge

EMERGENCY ENTRANCE (24/7):
- Dedicated emergency entrance with ambulance bay
- Direct access for walk-in emergency patients
- Wheelchair accessible with automatic doors
- Emergency parking spaces available directly outside

WHEN TO CALL 911:
• Chest pain or difficulty breathing
• Severe injuries or trauma
• Loss of consciousness
• Severe allergic reactions
• Signs of stroke (sudden numbness, confusion, severe headache)
• Any life-threatening emergency

VISITOR INFORMATION
-------------------
VISITING HOURS:
- General visiting hours: 8:00 AM to 8:00 PM daily
- ICU visiting hours: 10:00 AM to 2:00 PM, 6:00 PM to 8:00 PM
- Pediatric ward: Parents/guardians welcome 24/7
- One visitor at a time per patient (exceptions for end-of-life care)

PARKING:
${parking}
- First 2 hours free for visitors
- Validation available at information desk
- Handicap accessible spaces available

PATIENT SERVICES & AMENITIES
-----------------------------
• 24/7 Cafeteria with healthy meal options
• Gift shop with flowers, cards, and comfort items
• Chapel/meditation room for all faiths
• WiFi throughout the facility (Network: ${hospital_name// /}_Guest)
• Patient advocate services
• Discharge planning and social services
• Pharmacy on-site for prescription needs
• ATM and banking services in main lobby

CONTACT INFORMATION
-------------------
Main Hospital Number: (555) $(printf "%03d" $((RANDOM % 900 + 100)))-$(printf "%04d" $((RANDOM % 9000 + 1000)))
Emergency Department Direct: (555) $(printf "%03d" $((RANDOM % 900 + 100)))-$(printf "%04d" $((RANDOM % 9000 + 1000)))
Patient Information: (555) $(printf "%03d" $((RANDOM % 900 + 100)))-$(printf "%04d" $((RANDOM % 9000 + 1000)))
Billing Inquiries: (555) $(printf "%03d" $((RANDOM % 900 + 100)))-$(printf "%04d" $((RANDOM % 9000 + 1000)))

IMPORTANT REMINDERS
-------------------
• Bring a valid photo ID and insurance cards for all appointments
• Arrive 15 minutes early for scheduled appointments
• Keep a list of current medications and allergies with you
• Designate a healthcare proxy and ensure we have emergency contact information
• Ask questions - our staff is here to help explain your care

For life-threatening emergencies, always call 911 first.
For urgent but non-life-threatening issues, contact your primary care physician 
or visit our emergency department.

================================================================================
Last updated: $(date +"%B %Y")
================================================================================
EOF

    echo "Created: $filename"
}

# Main execution
echo "Generating hospital information files..."
echo "========================================"

for hospital in "${hospitals[@]}"; do
    create_hospital_file "$hospital"
done

echo ""
echo "All hospital information files have been generated successfully!"
echo "Files are ready for RAG system ingestion."