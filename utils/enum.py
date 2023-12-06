from enum import Enum

class RoleEnum(Enum):
    superadmin=1
    user = 2


class GenderEnum(Enum):
    male = "Male"
    female = "Female"
    Not_to_say = None
    
    

class SocialTypeEnum(Enum):
    google = 1
    facebook = 2
    instagram = 3
    apple = 4
    twitter = 5
    

class StaticEnum(Enum):
    forget_otp ="ForgetOtp"
    forget_password_otp ="Otp"
    forget_password_email ="Email"
    email_verify ="EmailVerify"
    forget_link="Link"
    cash_on_hand ="COH"
    pending = "Pending"
    in_progress = "In-Progress"
    admin = "Admin"
    procurement = "Procurement"
    new = "New"
    requested = "Requested"
    timeformatT = "%Y-%m-%dT%H:%M:%S"
    accepted = "Accepted"
    completed = "Completed"
    rejected = "Rejected"
    bussiness = 2
    questions = 1
    job = "Job"