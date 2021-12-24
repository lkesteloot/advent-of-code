class Scratch {
    public static void bar(
            int w0,
            int w1,
            int w2,
            int w3,
            int w4,
            int w5,
            int w6,
            int w7,
            int w8,
            int w9,
            int w10,
            int w11,
            int w12,
            int w13) {

        if (w0 < 1 || w0 > 9) return;
        if (w1 < 1 || w1 > 9) return;
        if (w2 < 1 || w2 > 9) return;
        if (w3 < 1 || w3 > 9) return;
        if (w4 < 1 || w4 > 9) return;
        if (w5 < 1 || w5 > 9) return;
        if (w6 < 1 || w6 > 9) return;
        if (w7 < 1 || w7 > 9) return;
        if (w8 < 1 || w8 > 9) return;
        if (w9 < 1 || w9 > 9) return;
        if (w10 < 1 || w10 > 9) return;
        if (w11 < 1 || w11 > 9) return;
        if (w12 < 1 || w12 > 9) return;
        if (w13 < 1 || w13 > 9) return;

        int x;
        int z;

        z = w0 + 10;
        // z = w0 + 10
        z = z*26 + w1 + 16;
        // z = (w0 + 10)*26 + w1 + 16
        z = z*26 + w2;
        // z = ((w0 + 10)*26 + w1 + 16)*26 + w2
        z = z*26 + w3 + 13;
        // z = (((w0 + 10)*26 + w1 + 16)*26 + w2)*26 + w3 + 13
        x = w3 + 13 + -14;
        z /= 26;
        // z = ((w0 + 10)*26 + w1 + 16)*26 + w2
        if (x != w4) { // w3 - 1 = w4, w3 = w4 + 1
            // Does not happen.
            z = z*26 + w4 + 7;
        }
        x = z%26 + -4; // x = w2 - 4
        z /= 26;
        // z = (w0 + 10)*26 + w1 + 16
        if (x != w5) { // w2 - 4 = w5, w2 = w5 + 4
            z = z*26 + w5 + 11;
        }

        z = z*26 + w6 + 11;
        // z = ((w0 + 10)*26 + w1 + 16)*26 + w6 + 11
        x = z%26 + -3; // w6 + 11 - 3 = w6 + 8
        z /= 26;
        // z = (w0 + 10)*26 + w1 + 16
        if (x != w7) { // w6 + 8 = w7
            z = z*26 + w7 + 10;
        }
        z = z*26 + w8 + 16;
        // z = ((w0 + 10)*26 + w1 + 16)*26 + w8 + 16
        x = z%26 + -12; // w8 + 16 - 12 = w8 + 4
        z /= 26;
        // z = (w0 + 10)*26 + w1 + 16
        if (x != w9) { // w8 + 4 = w9
            z = z*26 + w9 + 8;
        }
        z = z*26 + w10 + 15;
        // z = ((w0 + 10)*26 + w1 + 16)*26 + w10 + 15
        x = z%26 + -12; // w10 + 15 - 12 = w10 + 3
        z /= 26;
        // z = (w0 + 10)*26 + w1 + 16
        if (x != w11) { // w10 + 3 = w11
            z = z*26 + w11 + 2;
        }
        x = z%26 + -15; // w1 + 16 - 15 = w1 + 1
        z /= 26;
        // z = w0 + 10
        if (x != w12) { // w1 + 1 = w12
            z = z*26 + w12 + 5;
        }
        x = z%26 + -12; // w0 + 10 - 12 = w0 - 2
        z /= 26;
        // z = 0
        if (x != w13) { // w0 - 2 = w13, w0 = w13 + 2
            z = z*26 + w13 + 10;
        }
    }
}


