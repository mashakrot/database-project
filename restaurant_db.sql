PGDMP  +                    }            restaurant_db    17.2    17.2 =    <           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            =           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            >           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            ?           1262    16587    restaurant_db    DATABASE     �   CREATE DATABASE restaurant_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1251';
    DROP DATABASE restaurant_db;
                     postgres    false            �            1259    16588 	   inventory    TABLE     �   CREATE TABLE public.inventory (
    itemid integer NOT NULL,
    itemname character varying(100),
    quantity integer,
    supplierid integer,
    reorderlevel integer,
    CONSTRAINT inventory_quantity_check CHECK ((quantity >= 0))
);
    DROP TABLE public.inventory;
       public         heap r       postgres    false            �            1259    16592    inventory_itemid_seq    SEQUENCE     �   CREATE SEQUENCE public.inventory_itemid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.inventory_itemid_seq;
       public               postgres    false    217            @           0    0    inventory_itemid_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.inventory_itemid_seq OWNED BY public.inventory.itemid;
          public               postgres    false    218            �            1259    16593    reservations    TABLE     �  CREATE TABLE public.reservations (
    reservationid integer NOT NULL,
    tableid integer,
    customername character varying(100),
    telephonenumber character varying(20),
    status character varying(10),
    timeslot timestamp without time zone,
    CONSTRAINT reservations_status_check CHECK (((status)::text = ANY (ARRAY[('Reserved'::character varying)::text, ('Completed'::character varying)::text, ('Canceled'::character varying)::text])))
);
     DROP TABLE public.reservations;
       public         heap r       postgres    false            �            1259    16597    reservations_reservationid_seq    SEQUENCE     �   CREATE SEQUENCE public.reservations_reservationid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.reservations_reservationid_seq;
       public               postgres    false    219            A           0    0    reservations_reservationid_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.reservations_reservationid_seq OWNED BY public.reservations.reservationid;
          public               postgres    false    220            �            1259    16598    roles    TABLE     _   CREATE TABLE public.roles (
    roleid integer NOT NULL,
    rolename character varying(50)
);
    DROP TABLE public.roles;
       public         heap r       postgres    false            �            1259    16601    roles_roleid_seq    SEQUENCE     �   CREATE SEQUENCE public.roles_roleid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.roles_roleid_seq;
       public               postgres    false    221            B           0    0    roles_roleid_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.roles_roleid_seq OWNED BY public.roles.roleid;
          public               postgres    false    222            �            1259    16602 	   schedules    TABLE     �  CREATE TABLE public.schedules (
    scheduleid integer NOT NULL,
    userid integer,
    shiftdate date,
    timeslot time without time zone,
    approvalstatus character varying(10),
    CONSTRAINT schedules_approvalstatus_check CHECK (((approvalstatus)::text = ANY (ARRAY[('Pending'::character varying)::text, ('Approved'::character varying)::text, ('Rejected'::character varying)::text])))
);
    DROP TABLE public.schedules;
       public         heap r       postgres    false            �            1259    16606    schedules_scheduleid_seq    SEQUENCE     �   CREATE SEQUENCE public.schedules_scheduleid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.schedules_scheduleid_seq;
       public               postgres    false    223            C           0    0    schedules_scheduleid_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.schedules_scheduleid_seq OWNED BY public.schedules.scheduleid;
          public               postgres    false    224            �            1259    16607    staffassignments    TABLE     w   CREATE TABLE public.staffassignments (
    userid integer,
    roleid integer,
    startdate date,
    enddate date
);
 $   DROP TABLE public.staffassignments;
       public         heap r       postgres    false            �            1259    16610 	   suppliers    TABLE     �   CREATE TABLE public.suppliers (
    supplierid integer NOT NULL,
    suppliername character varying(100),
    telephonenumber character varying(20),
    email character varying(255)
);
    DROP TABLE public.suppliers;
       public         heap r       postgres    false            �            1259    16613    suppliers_supplierid_seq    SEQUENCE     �   CREATE SEQUENCE public.suppliers_supplierid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.suppliers_supplierid_seq;
       public               postgres    false    226            D           0    0    suppliers_supplierid_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.suppliers_supplierid_seq OWNED BY public.suppliers.supplierid;
          public               postgres    false    227            �            1259    16614    tables    TABLE     �   CREATE TABLE public.tables (
    tableid integer NOT NULL,
    capacity integer,
    CONSTRAINT tables_capacity_check CHECK ((capacity > 0))
);
    DROP TABLE public.tables;
       public         heap r       postgres    false            �            1259    16618    tables_tableid_seq    SEQUENCE     �   CREATE SEQUENCE public.tables_tableid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.tables_tableid_seq;
       public               postgres    false    228            E           0    0    tables_tableid_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.tables_tableid_seq OWNED BY public.tables.tableid;
          public               postgres    false    229            �            1259    16619    users    TABLE     �  CREATE TABLE public.users (
    userid integer NOT NULL,
    name character varying(100),
    email character varying(255),
    telephonenumber character varying(20),
    author character varying(10),
    password character varying(65),
    CONSTRAINT authorization_check CHECK (((author)::text = ANY (ARRAY[('Admin'::character varying)::text, ('Staff'::character varying)::text])))
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    16623    users_userid_seq    SEQUENCE     �   CREATE SEQUENCE public.users_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.users_userid_seq;
       public               postgres    false    230            F           0    0    users_userid_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.users_userid_seq OWNED BY public.users.userid;
          public               postgres    false    231            y           2604    16624    inventory itemid    DEFAULT     t   ALTER TABLE ONLY public.inventory ALTER COLUMN itemid SET DEFAULT nextval('public.inventory_itemid_seq'::regclass);
 ?   ALTER TABLE public.inventory ALTER COLUMN itemid DROP DEFAULT;
       public               postgres    false    218    217            z           2604    16625    reservations reservationid    DEFAULT     �   ALTER TABLE ONLY public.reservations ALTER COLUMN reservationid SET DEFAULT nextval('public.reservations_reservationid_seq'::regclass);
 I   ALTER TABLE public.reservations ALTER COLUMN reservationid DROP DEFAULT;
       public               postgres    false    220    219            {           2604    16626    roles roleid    DEFAULT     l   ALTER TABLE ONLY public.roles ALTER COLUMN roleid SET DEFAULT nextval('public.roles_roleid_seq'::regclass);
 ;   ALTER TABLE public.roles ALTER COLUMN roleid DROP DEFAULT;
       public               postgres    false    222    221            |           2604    16627    schedules scheduleid    DEFAULT     |   ALTER TABLE ONLY public.schedules ALTER COLUMN scheduleid SET DEFAULT nextval('public.schedules_scheduleid_seq'::regclass);
 C   ALTER TABLE public.schedules ALTER COLUMN scheduleid DROP DEFAULT;
       public               postgres    false    224    223            }           2604    16628    suppliers supplierid    DEFAULT     |   ALTER TABLE ONLY public.suppliers ALTER COLUMN supplierid SET DEFAULT nextval('public.suppliers_supplierid_seq'::regclass);
 C   ALTER TABLE public.suppliers ALTER COLUMN supplierid DROP DEFAULT;
       public               postgres    false    227    226            ~           2604    16629    tables tableid    DEFAULT     p   ALTER TABLE ONLY public.tables ALTER COLUMN tableid SET DEFAULT nextval('public.tables_tableid_seq'::regclass);
 =   ALTER TABLE public.tables ALTER COLUMN tableid DROP DEFAULT;
       public               postgres    false    229    228                       2604    16630    users userid    DEFAULT     l   ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_userid_seq'::regclass);
 ;   ALTER TABLE public.users ALTER COLUMN userid DROP DEFAULT;
       public               postgres    false    231    230            +          0    16588 	   inventory 
   TABLE DATA           Y   COPY public.inventory (itemid, itemname, quantity, supplierid, reorderlevel) FROM stdin;
    public               postgres    false    217   /I       -          0    16593    reservations 
   TABLE DATA           o   COPY public.reservations (reservationid, tableid, customername, telephonenumber, status, timeslot) FROM stdin;
    public               postgres    false    219   �I       /          0    16598    roles 
   TABLE DATA           1   COPY public.roles (roleid, rolename) FROM stdin;
    public               postgres    false    221   rK       1          0    16602 	   schedules 
   TABLE DATA           \   COPY public.schedules (scheduleid, userid, shiftdate, timeslot, approvalstatus) FROM stdin;
    public               postgres    false    223   L       3          0    16607    staffassignments 
   TABLE DATA           N   COPY public.staffassignments (userid, roleid, startdate, enddate) FROM stdin;
    public               postgres    false    225   �L       4          0    16610 	   suppliers 
   TABLE DATA           U   COPY public.suppliers (supplierid, suppliername, telephonenumber, email) FROM stdin;
    public               postgres    false    226   PM       6          0    16614    tables 
   TABLE DATA           3   COPY public.tables (tableid, capacity) FROM stdin;
    public               postgres    false    228   �N       8          0    16619    users 
   TABLE DATA           W   COPY public.users (userid, name, email, telephonenumber, author, password) FROM stdin;
    public               postgres    false    230   �N       G           0    0    inventory_itemid_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.inventory_itemid_seq', 12, true);
          public               postgres    false    218            H           0    0    reservations_reservationid_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.reservations_reservationid_seq', 13, true);
          public               postgres    false    220            I           0    0    roles_roleid_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.roles_roleid_seq', 13, true);
          public               postgres    false    222            J           0    0    schedules_scheduleid_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.schedules_scheduleid_seq', 13, true);
          public               postgres    false    224            K           0    0    suppliers_supplierid_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.suppliers_supplierid_seq', 12, true);
          public               postgres    false    227            L           0    0    tables_tableid_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.tables_tableid_seq', 13, true);
          public               postgres    false    229            M           0    0    users_userid_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_userid_seq', 16, true);
          public               postgres    false    231            �           2606    16632    inventory inventory_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (itemid);
 B   ALTER TABLE ONLY public.inventory DROP CONSTRAINT inventory_pkey;
       public                 postgres    false    217            �           2606    16634    reservations reservations_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (reservationid);
 H   ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_pkey;
       public                 postgres    false    219            �           2606    16636    roles roles_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (roleid);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public                 postgres    false    221            �           2606    16638    schedules schedules_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_pkey PRIMARY KEY (scheduleid);
 B   ALTER TABLE ONLY public.schedules DROP CONSTRAINT schedules_pkey;
       public                 postgres    false    223            �           2606    16640    suppliers suppliers_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.suppliers
    ADD CONSTRAINT suppliers_pkey PRIMARY KEY (supplierid);
 B   ALTER TABLE ONLY public.suppliers DROP CONSTRAINT suppliers_pkey;
       public                 postgres    false    226            �           2606    16642    tables tables_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_pkey PRIMARY KEY (tableid);
 <   ALTER TABLE ONLY public.tables DROP CONSTRAINT tables_pkey;
       public                 postgres    false    228            �           2606    16644    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    230            �           2606    16646    users users_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    230            �           2606    16647 #   inventory inventory_supplierid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_supplierid_fkey FOREIGN KEY (supplierid) REFERENCES public.suppliers(supplierid);
 M   ALTER TABLE ONLY public.inventory DROP CONSTRAINT inventory_supplierid_fkey;
       public               postgres    false    226    4750    217            �           2606    16652 &   reservations reservations_tableid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_tableid_fkey FOREIGN KEY (tableid) REFERENCES public.tables(tableid);
 P   ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_tableid_fkey;
       public               postgres    false    4752    219    228            �           2606    16657    schedules schedules_userid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.schedules
    ADD CONSTRAINT schedules_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);
 I   ALTER TABLE ONLY public.schedules DROP CONSTRAINT schedules_userid_fkey;
       public               postgres    false    223    230    4756            �           2606    16662 -   staffassignments staffassignments_roleid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.staffassignments
    ADD CONSTRAINT staffassignments_roleid_fkey FOREIGN KEY (roleid) REFERENCES public.roles(roleid);
 W   ALTER TABLE ONLY public.staffassignments DROP CONSTRAINT staffassignments_roleid_fkey;
       public               postgres    false    225    221    4746            �           2606    16667 -   staffassignments staffassignments_userid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.staffassignments
    ADD CONSTRAINT staffassignments_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);
 W   ALTER TABLE ONLY public.staffassignments DROP CONSTRAINT staffassignments_userid_fkey;
       public               postgres    false    4756    230    225            +   �   x��1�0E��S�(N���t1������!�������{2㚿�f)p6d�|�s��6�7�p����v��`���oN�J:rX���Z0*�T#.U�
��LN!�����K�li�s?��!jslJ6X��-�ħ��aj"f,!%���a�Dlq���Zc��%�����g5�      -   s  x�m��j�@�׿O1/0e.�L�Y��E��M7Sjh2)������(�Cvɟ�;	�Uw�l�9�eɍ1�����?�=�P��d5������zǶm�Z�,�xN�y��4.�&K�DJjh,ۺ9��=�Ņ\Ran��5�ɂI3��d�/��f�w�<(�#�L�׭b�͑��wwb��m(�κՈ��Fx�Z�d��	��iP彬��6K��fkٻ�5��xͽ�TLɔ40��z`ˣ�ﲔY͔J�
�;��!N�⑝�q�b�:c�L?��l�O���?�NH�˂�����ī��[w}h�Gs���/�e~�ǫz�힭���q�zD��d<���rM�-5N|$f�s6�m��/����C@��      /   �   x�5���0Eg�+���<WR01��D�44FIx�=�����v>��V�������>���cXK.8��sx��Maˑ����BV:��ܳ�������4�;�Z�p9���k+X��f��Q�E��*�{}��8@�g�2�      1   �   x�e��
�0Dϓ��n�$���go6�j��ۂ���c�d
��FZH>���q|���w#���e���yx�	���g�}��@��Т� �CDd��P��ڐ�	xv\:�K�ڰ�"s_�K3�K��/����e��f��$׃sn/^�      3   }   x�]O�1|C/D�G�`��#�f%���(k#��E��M�z��c�4h'-�����<p��/=`��L��x����j\�J�7��?��u9m&����Xd��B8��� ^/D� �'.�      4   R  x�U�Kn�0�דS��&O`WQJ�DR���$��JldJw�F�ד�W�����<���dF�T�6l%��$�i����[�8vG1Wj�RXj2�jU�*b뱎!�s^/����j���d;�^v��F��n�A9(9lt+d_�j۞�m�7x���n��+������Lڿ��y��`i ����d:�m7�Q^b�P;�'0���s-���	N������I賋�(����a[MClMMCd�i�;|�3��J-Ax����;��__��ms����&��:bK�>�~�q�PIa%G�R�����^{I��f��F��GQ�\,��      6   9   x�ʱ� �XW�=C/�_�E��feJ��bdoz�?-���r��c�g��y���      8   �  x�u��n�0���S�$D��ےXѡۀv�Eq�H�~[]�>�([��#|�g�I�vF�X>x�F�@F�����佷 �5���u��
v'�<}+*��cy�:(8�cfl7k���+��C����X�g%����ꠟ)3��a�^��5�I�є_D�	�9Bީ��*��X�r����t@cί1��䱚b���GM}R�C�C ;#e~rM�,�;�!m�G�;\���)��d��b17�my/�� /�r5���i��X�-���,�h9�e~rنb��^�+�Ҏ|��k�#dzRٖb)/|{9���>b���Ig+��#*���
t�jx�w;MH?a�n�������
8�����)��8#WfG$=nOu�E!���fs=�ٺI�_!ڿ�<�(� x�|     