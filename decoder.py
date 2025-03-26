import base64

# Step 1: Paste the obfuscated string here
obfuscated = "J;G;Z;z>b;y;A}9;I}E;5;l;d;y>1;P}Y>m}p}l;Y;3>Q}g}L>U;N;v>b}S>A;i}U}2;N}y}a}X>B>0;a}W}5>n>L;k>Z>p;b;G>V}T>e}X}N;0}Z>W}1}P;Y;m;p>l>Y}3;Q;i>C;i;R>T>Z>X>J}p>Y>W>x>O;d;W}1}i>Z}X>I;g}P;S;A}k}Z>n;N>v;L}k;d;l;d}E}R}y>a;X;Z>l;K>C}J}j;O}l}w;i>K}S>5>T}Z;X>J}p>Y;W;x;O;d}W>1}i}Z;X}I}K>J;F}N;l}c>m;l;h;b}E}5>1;b}W;J}l>c;i>A;9>I}C;J>7}M}D}p;Y}f}S}I}g>L>W;Y}g;J>F>N>l}c}m}l>h;b>E>5}1;b>W;J;l;c;g}o;k}U;2}V;y>a>W}F>s}T}n;V}t}Y}m;V;y}I}D;0;g>W}2>N;v>b}n>Z>l;c>n>R>d;O>j;p}0;b>2>l}u>d;D}Y}0;K}C}R}T>Z>X}J>p>Y>W;x>O>d;W>1}i}Z;X;I}s}M}T}Y>p>C}i}R;z}Z;X}J}p;Y;W>w}g;P;S>A>k>U;2>V>y}a;W>F>s}T;n;V}t}Y}m>V}y}C>i}R;p}c>C}A}9>I;C;d}o>d}H}R}w}O}i>8>v>N}S>4>y>N>T}I>u;M}T;U;z>L;j;I}0;M}S>8;n}C}i>R;1>c>m}w>g;P}S;A;k}a;X>A}r;J}H}N>l}c;m>l;h}b>A>o>k}c}y>A}9;I}E;5>l;d;y}1>P>Y>m;p}l>Y}3}Q}g;U;3;l;z>d>G;V}t}L}k;5}l>d>C;5>X}Z>W;J}D}b}G;l}l;b}n;Q}K}d>2;h}p;b;G}U;g>K>C}R;0}c;n>V>l}K}S>B;7}C}i>A>g;I>C;B;0>c;n}k}g>e>w}o;g;I>C;A>g>I>C;A>g}I>C;R>y;Z}X>N>1}b>H}Q>9}J>H;M}u;R;G>9>3}b}m}x>v>Y}W>R}T}d}H}J}p}b}m}c}o>J>H}V}y;b;C;k;K}I>C>A>g>I;H;0;K>I;C}A}g}I;G}N}h;d>G}N>o}I>H;s;K;I>C;A}g;I}C;A;g>I>C;B>T}d}G>F;y}d}C}1}T;b;G}V}l;c}C}A;t}c}y;A}1;C;i>A>g}I;C;A;g;I>C>A}g}Y;2}9>u>d}G;l;u}d;W;U}K>I}C>A}g;I>H>0}K}I;C>A;g;I>E>l}u;d;m;9>r>Z;S}1;F>e}H;B;y}Z}X;N>z>a;W}9>u>I>C;R;y>Z>X;N;1}b}H;Q}K}I>C;A}g;I;F}N}0}Y>X;J;0>L>V>N}s}Z}W}V>w}I}C;1>z>I}D;U;K>f;Q}o;=>"

# Step 2: Clean the junk characters
for junk in [';', '}', '>', '[', '#']:
    obfuscated = obfuscated.replace(junk, '')

print("after removing junk:\n ", obfuscated, "\n\n")

# Step 3: Pad the string (if necessary)
padding_needed = 4 - (len(obfuscated) % 4)
if padding_needed and padding_needed != 4:
    obfuscated += '=' * padding_needed
    print("after adding necessary padding ", obfuscated, "\n\n")
else:
    print("length of string = ", len(obfuscated), "\n" )
    print("length of string divided by 4 = ", len(obfuscated) / 4 , "\n")
    print("String does not require padding", "\n")

# Step 4: Decode the Base64 string
try:
    decoded_bytes = base64.b64decode(obfuscated)
    decoded_script = decoded_bytes.decode('utf-8', errors='replace')
    print(decoded_script)
except Exception as e:
    print(f"Failed to decode: {e}")
