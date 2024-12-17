# f5_auth


# làm luồng create đăng ký
+ type email
+ check user đã được đăng kí chưa
+ check user đã được email xác nhận chưa
+ check expired password
+ send mail
+ return retry_time, refresh_token
# làm luồng confirm đăng ký
+ type password
+ check paswowrd
+ create user user
+ return user_info, access_token
# làm luồng thay đổi password
+ type old password, new password
+ check password
+ return new_token

