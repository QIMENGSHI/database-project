PGDMP     $    6                |            sosadatabase    15.1    15.1                 0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                        0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            !           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            "           1262    74433    sosadatabase    DATABASE     �   CREATE DATABASE sosadatabase WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Finland.1252';
    DROP DATABASE sosadatabase;
                postgres    false            �            1259    74449    event    TABLE     �   CREATE TABLE public.event (
    eventid integer NOT NULL,
    eventname character varying(255) NOT NULL,
    eventdate date NOT NULL
);
    DROP TABLE public.event;
       public         heap    postgres    false            �            1259    74448    event_eventid_seq    SEQUENCE     �   CREATE SEQUENCE public.event_eventid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.event_eventid_seq;
       public          postgres    false    217            #           0    0    event_eventid_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.event_eventid_seq OWNED BY public.event.eventid;
          public          postgres    false    216            �            1259    74488    eventregistration    TABLE     �   CREATE TABLE public.eventregistration (
    registrationid integer NOT NULL,
    membershipid integer,
    eventid integer NOT NULL
);
 %   DROP TABLE public.eventregistration;
       public         heap    postgres    false            �            1259    74487 $   eventregistration_registrationid_seq    SEQUENCE     �   CREATE SEQUENCE public.eventregistration_registrationid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.eventregistration_registrationid_seq;
       public          postgres    false    220            $           0    0 $   eventregistration_registrationid_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.eventregistration_registrationid_seq OWNED BY public.eventregistration.registrationid;
          public          postgres    false    219            �            1259    74434 
   membership    TABLE     �   CREATE TABLE public.membership (
    membershipid integer NOT NULL,
    membershiptype character varying(255) NOT NULL,
    startdate date NOT NULL,
    expiredate date NOT NULL
);
    DROP TABLE public.membership;
       public         heap    postgres    false            �            1259    74439    student    TABLE     �   CREATE TABLE public.student (
    studentid integer NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL
);
    DROP TABLE public.student;
       public         heap    postgres    false            �            1259    74455    studentmembership    TABLE     m   CREATE TABLE public.studentmembership (
    studentid integer NOT NULL,
    membershipid integer NOT NULL
);
 %   DROP TABLE public.studentmembership;
       public         heap    postgres    false            v           2604    74452    event eventid    DEFAULT     n   ALTER TABLE ONLY public.event ALTER COLUMN eventid SET DEFAULT nextval('public.event_eventid_seq'::regclass);
 <   ALTER TABLE public.event ALTER COLUMN eventid DROP DEFAULT;
       public          postgres    false    216    217    217            w           2604    74491     eventregistration registrationid    DEFAULT     �   ALTER TABLE ONLY public.eventregistration ALTER COLUMN registrationid SET DEFAULT nextval('public.eventregistration_registrationid_seq'::regclass);
 O   ALTER TABLE public.eventregistration ALTER COLUMN registrationid DROP DEFAULT;
       public          postgres    false    220    219    220                      0    74449    event 
   TABLE DATA           >   COPY public.event (eventid, eventname, eventdate) FROM stdin;
    public          postgres    false    217   &                 0    74488    eventregistration 
   TABLE DATA           R   COPY public.eventregistration (registrationid, membershipid, eventid) FROM stdin;
    public          postgres    false    220   A&                 0    74434 
   membership 
   TABLE DATA           Y   COPY public.membership (membershipid, membershiptype, startdate, expiredate) FROM stdin;
    public          postgres    false    214   ^&                 0    74439    student 
   TABLE DATA           9   COPY public.student (studentid, name, email) FROM stdin;
    public          postgres    false    215   �&                 0    74455    studentmembership 
   TABLE DATA           D   COPY public.studentmembership (studentid, membershipid) FROM stdin;
    public          postgres    false    218   �&       %           0    0    event_eventid_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.event_eventid_seq', 5, true);
          public          postgres    false    216            &           0    0 $   eventregistration_registrationid_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.eventregistration_registrationid_seq', 1, true);
          public          postgres    false    219                       2606    74454    event event_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (eventid);
 :   ALTER TABLE ONLY public.event DROP CONSTRAINT event_pkey;
       public            postgres    false    217            �           2606    74493 (   eventregistration eventregistration_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.eventregistration
    ADD CONSTRAINT eventregistration_pkey PRIMARY KEY (registrationid);
 R   ALTER TABLE ONLY public.eventregistration DROP CONSTRAINT eventregistration_pkey;
       public            postgres    false    220            y           2606    74438    membership membership_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.membership
    ADD CONSTRAINT membership_pkey PRIMARY KEY (membershipid);
 D   ALTER TABLE ONLY public.membership DROP CONSTRAINT membership_pkey;
       public            postgres    false    214            {           2606    74447    student student_email_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_email_key UNIQUE (email);
 C   ALTER TABLE ONLY public.student DROP CONSTRAINT student_email_key;
       public            postgres    false    215            }           2606    74445    student student_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (studentid);
 >   ALTER TABLE ONLY public.student DROP CONSTRAINT student_pkey;
       public            postgres    false    215            �           2606    74459 (   studentmembership studentmembership_pkey 
   CONSTRAINT     {   ALTER TABLE ONLY public.studentmembership
    ADD CONSTRAINT studentmembership_pkey PRIMARY KEY (studentid, membershipid);
 R   ALTER TABLE ONLY public.studentmembership DROP CONSTRAINT studentmembership_pkey;
       public            postgres    false    218    218            �           2606    74499 0   eventregistration eventregistration_eventid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.eventregistration
    ADD CONSTRAINT eventregistration_eventid_fkey FOREIGN KEY (eventid) REFERENCES public.event(eventid) ON DELETE CASCADE;
 Z   ALTER TABLE ONLY public.eventregistration DROP CONSTRAINT eventregistration_eventid_fkey;
       public          postgres    false    220    3199    217            �           2606    74494 5   eventregistration eventregistration_membershipid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.eventregistration
    ADD CONSTRAINT eventregistration_membershipid_fkey FOREIGN KEY (membershipid) REFERENCES public.membership(membershipid);
 _   ALTER TABLE ONLY public.eventregistration DROP CONSTRAINT eventregistration_membershipid_fkey;
       public          postgres    false    3193    220    214            �           2606    74465 5   studentmembership studentmembership_membershipid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.studentmembership
    ADD CONSTRAINT studentmembership_membershipid_fkey FOREIGN KEY (membershipid) REFERENCES public.membership(membershipid);
 _   ALTER TABLE ONLY public.studentmembership DROP CONSTRAINT studentmembership_membershipid_fkey;
       public          postgres    false    218    214    3193            �           2606    74460 2   studentmembership studentmembership_studentid_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.studentmembership
    ADD CONSTRAINT studentmembership_studentid_fkey FOREIGN KEY (studentid) REFERENCES public.student(studentid);
 \   ALTER TABLE ONLY public.studentmembership DROP CONSTRAINT studentmembership_studentid_fkey;
       public          postgres    false    218    215    3197               *   x�3�,.-H-RH+�SH-K�+�4202�50�54������ �{�            x������ � �         1   x�343524���/�M�Q�M�MJ-�4202�50�501�!L�=... 2�
�         .   x�3426153�����O���O��M�MtH�M���K������� �|
}            x�3426153���443524����� 0P�     