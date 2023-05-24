from rest_framework import serializers

def password_match_checker(password, passworc_confirm):
    if password != passworc_confirm:
        raise serializers.ValidationError("Passwords arent match")
    return 1
