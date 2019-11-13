#include <stdio.h>
#include <errno.h>
#include "UserInformation.pb-c.h"

static size_t pack_user_data(uint8_t *buffer)
{
    UserInformation userInfo;

    user_information__init(&userInfo);

    userInfo.name = "Benjamin";
    userInfo.age = 18;    
    userInfo.phone = "0755-12345678";
    userInfo.stat = USER_STATUS__IDLE;
    userInfo.email = "ZhangSan@123.com";

    return user_information__pack(&userInfo, buffer);
}

static size_t unpack_user_data(const uint8_t *buffer, size_t len)
{
    UserInformation *userInfo =  user_information__unpack(NULL, len, buffer);
    if(!userInfo){
        printf("user_information__unpack is fail!!!\n");
        return 1;
    }

    printf("Unpack: %s %d %s %s\n", userInfo->name, userInfo->age, userInfo->phone, userInfo->email);
    user_information__free_unpacked(userInfo, NULL);

    return 0;
}

int main()
{
    uint8_t buffer[1024];
    
    size_t lenght = pack_user_data(buffer);
    printf("User data len: %ld\n",lenght);
    unpack_user_data(buffer, lenght);
	
	return 0;
}


