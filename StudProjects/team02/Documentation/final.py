import sys
sys.path.append('../')
from pycore.tikzeng import *

# defined your arch
arch = [
    to_head( '..' ),
    to_cor(),
    to_begin(),
    to_input('20150703_0810_45.jpg'),

    to_Conv( name='conv1', s_filer=150, n_filer=32, offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=40 ),
    to_Pool("pool1", offset="(3,0,0)", to="(conv1-east)", width=5, height=24, caption="MaxPooling"),
    to_connection( "conv1", "pool1"), 
    to_UnPool(name="flat1", offset="(2,0,0)", to="(pool1-east)",  depth=86, height=3, width=1, caption="Flatten"),
    to_connection("pool1", "flat1"),
    to_ConvSoftMax( name='dense1', s_filer=512, offset="(2,0,0)", to="(flat1-east)", depth=86, height=3, width=3, caption="Dense"),
    to_connection("flat1", "dense1"),
    to_SoftMax("soft1", 2 ,"(3,0,0)", to="(dense1-east)", depth=12, height=3, width=3, caption="SOFTMAX"),   
    to_connection( "dense1", "soft1"), 
    to_end()
    ]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
