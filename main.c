#include "packets.h"
#include <stdio.h>

const unsigned char *packets[66] = {
    pkt001, pkt003, pkt005, pkt007, pkt009, pkt011, pkt013, pkt015, pkt017,
    pkt019, pkt021, pkt023, pkt025, pkt027, pkt029, pkt031, pkt033, pkt035,
    pkt037, pkt039, pkt041, pkt043, pkt045, pkt047, pkt049, pkt051, pkt053,
    pkt055, pkt057, pkt059, pkt061, pkt063, pkt065, pkt067, pkt069, pkt071,
    pkt073, pkt075, pkt077, pkt079, pkt081, pkt083, pkt085, pkt087, pkt089,
    pkt091, pkt093, pkt095, pkt097, pkt099, pkt101, pkt103, pkt105, pkt107,
    pkt109, pkt111, pkt113, pkt115, pkt117, pkt119, pkt121, pkt123, pkt125,
    pkt127, pkt129, pkt131,
};

unsigned char distance(unsigned char a, unsigned char b) {
    if (a > b)
        return a - b;
    else
        return b - a;
}
int main(int argc, char *argv[]) {
    for (int i = 0; i < 22; i++) {
        for (int j = 0; j < 8; j++) {
            printf("%02X", packets[i + 22 * 0][j]);
        }
        printf("	");
        for (int j = 0; j < 8; j++) {
            printf("%02X", packets[i + 22 * 1][j]);
        }
        printf("	");
        for (int j = 0; j < 8; j++) {
            printf("%02X", distance(packets[i + 22][j], packets[i][j]));
        }
        printf("	");
        printf("\n");
    }
}
