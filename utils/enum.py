from enum import Enum

class RoleEnum(Enum):
    superadmin=1
    tenant = 2


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
    timeformatT = "%Y-%m-%dT%H:%M:%S"
    accepted = "Accepted"
    completed = "Completed"
    rejected = "Rejected"
    
class UnintsEnum(Enum):
    one_bhk = "1BHK"
    two_bhk = "2BHK"
    three_bhk = "3BHK"
