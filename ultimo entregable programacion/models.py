from collections import deque
from datetime import datetime
import re

class Patient:
    def __init__(self, id_card, name, phone, client_type, attention_type, quantity, priority, appointment_date, appointment_time, total_value):
        self.id_card = id_card
        self.name = name
        self.phone = phone
        self.client_type = client_type
        self.attention_type = attention_type
        self.quantity = quantity
        self.priority = priority
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.total_value = total_value
        self.timestamp = datetime.now()
        self.gender = self._infer_gender(name)
        
    def _infer_gender(self, name):
        """Infers the gender based on the first name to assign an avatar."""
        # Get the first word as the first name
        first_name = name.split()[0].lower()
        
        # Explicit lists of common names to handle exceptions
        common_female = ['mary', 'anna', 'laura', 'martha', 'helen', 'diana', 'sophia', 'isabella', 'mia', 'emma', 'olivia', 'ava', 'charlotte', 'amelia', 'harper', 'evelyn', 'abigail', 'emily', 'elizabeth', 'mila', 'ella', 'avery', 'sofia', 'camila', 'aria', 'scarlett', 'victoria', 'madison', 'luna', 'grace', 'chloe', 'penelope', 'layla', 'riley', 'zoey', 'nora', 'lily', 'eleanor', 'hannah', 'lillian', 'addison', 'aubrey', 'ellie', 'stella', 'natalie', 'zoe', 'leah', 'hazel', 'violet', 'aurora', 'savannah', 'audrey', 'brooklyn', 'bella', 'claire', 'skylar', 'lucy', 'paisley', 'everly', 'anna', 'caroline', 'nova', 'genesis', 'emilia', 'kennedy', 'samantha', 'maya', 'willow', 'kinsley', 'naomi', 'aaliyah', 'elena', 'sarah', 'ariana', 'allison', 'gabriella', 'alice', 'madelyn', 'cora', 'ruby', 'eva', 'serenity', 'autumn', 'adeline', 'hailey', 'gianna', 'valentina', 'isla', 'eliana', 'quinn', 'nevaeh', 'ivy', 'sadie', 'piper', 'lydia', 'alexa', 'josephine', 'emery', 'julia', 'delilah', 'arianna', 'vivian', 'kaylee', 'sophie', 'brielle', 'madeline']
        common_male = ['john', 'charles', 'luis', 'george', 'peter', 'andrew', 'liam', 'noah', 'william', 'james', 'oliver', 'benjamin', 'elijah', 'lucas', 'mason', 'logan', 'alexander', 'ethan', 'jacob', 'michael', 'daniel', 'henry', 'jackson', 'sebastian', 'aiden', 'matthew', 'samuel', 'david', 'joseph', 'carter', 'owen', 'wyatt', 'cameron', 'luke', 'jayden', 'dylan', 'grayson', 'levi', 'isaac', 'gabriel', 'julian', 'mateo', 'anthony', 'jaxon', 'lincoln', 'joshua', 'christopher', 'andrew', 'theodore', 'caleb', 'ryan', 'asher', 'nathan', 'thomas', 'leo', 'isaiah', 'charles', 'josiah', 'hudson', 'christian', 'hunter', 'connor', 'eli', 'ezra', 'aaron', 'landon', 'adrian', 'jonathan', 'nolan', 'jeremiah', 'easton', 'elias', 'colton', 'cameron', 'carson', 'robert', 'angel', 'maverick', 'nicholas', 'dominic', 'jaxson', 'greyson', 'adam', 'ian', 'austin', 'santiago', 'jordan', 'cooper', 'brayden', 'roman', 'evan', 'ezekiel', 'xander', 'jose', 'jace', 'jameson', 'leonardo', 'bryson', 'axel', 'everett', 'parker', 'kayden', 'miles', 'sawyer', 'jason']

        if first_name in common_female:
            return 'female'
        elif first_name in common_male:
            return 'male'
            
        # Fallback to rules: names ending in 'a' are often female (especially in Spanish/Latin contexts)
        if first_name.endswith('a'):
            return 'female'
            
        # Default to male if unknown
        return 'male'

class Clinic:
    def __init__(self):
        self.clients = []
        self.daily_queue = deque()
        self.contingency_stack = []

    def register_patient(self, patient):
        self.clients.append(patient)
        self.daily_queue.append(patient)
        self._sort_daily_queue()
        
        # If extraction and urgent, add to stack
        if patient.attention_type == 'Extraction' and patient.priority == 'Urgent':
            self.contingency_stack.append(patient)
            self._sort_contingency_stack()

    def _sort_daily_queue(self):
        # Sort FIFO queue by date and time (earliest first)
        temp_queue = sorted(list(self.daily_queue), key=lambda x: (x.appointment_date, x.appointment_time))
        self.daily_queue.clear()
        self.daily_queue.extend(temp_queue)

    def _sort_contingency_stack(self):
        # Sort the stack so that the closest date and time is at the END (top of the stack)
        self.contingency_stack.sort(key=lambda x: (x.appointment_date, x.appointment_time), reverse=True)

    def attend_next_in_queue(self):
        if self.daily_queue:
            patient = self.daily_queue.popleft()
            # Remove from contingency stack if also present there
            if patient in self.contingency_stack:
                self.contingency_stack.remove(patient)
            return patient
        return None

    def attend_next_urgency(self):
        if self.contingency_stack:
            patient = self.contingency_stack.pop()
            # Remove from daily queue if also present there
            if patient in self.daily_queue:
                self.daily_queue.remove(patient)
            return patient
        return None

    def get_clients_sorted_by_value(self):
        return sorted(self.clients, key=lambda x: x.total_value, reverse=True)
