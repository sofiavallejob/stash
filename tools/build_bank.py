# Generates abstractions/bank.pd. Run from repo root: python3 tools/build_bank.py
objs=[]; ids={}; conns=[]
def o(n,x,y,t,k='obj'): ids[n]=len(objs); objs.append(f"#X {k} {x} {y} {t};")
def m(n,x,y,t): o(n,x,y,t,'msg')
def c(a,ao,b,bi): conns.append((a,ao,b,bi))
D='\\$0-data'

o('in',30,30,'inlet'); o('rt',30,70,'route store recall morph write read clear'); c('in',0,'rt',0)
o('out',30,1400,'outlet')
o('txt',1700,600,f'text define {D}')

def event(prefix,n,x,y,src,srco,slotsrc,slotso):
    o(n+'_f',x,y,'f'); o(n+'_p',x,y+40,'list prepend '+prefix); o(n+'_t',x,y+80,'list trim')
    c(slotsrc,slotso,n+'_f',1); c(src,srco,n+'_f',0)
    c(n+'_f',0,n+'_p',0); c(n+'_p',0,n+'_t',0); c(n+'_t',0,'out',0)

def iterator(p,x,y):
    # bang into p_t -> every line of the text, unpacked: slot name value
    o(p+'_t',x,y,'t b b'); m(p+'_z',x+80,y+40,'0')
    o(p+'_size',x,y+80,f'text size {D}'); o(p+'_u',x,y+120,'until')
    o(p+'_c',x,y+160,'f'); o(p+'_inc',x+60,y+160,'+ 1')
    o(p+'_get',x,y+200,f'text get {D}'); o(p+'_unp',x,y+240,'unpack f s f')
    c(p+'_t',1,p+'_z',0); c(p+'_z',0,p+'_c',1)
    c(p+'_t',0,p+'_size',0); c(p+'_size',0,p+'_u',0)
    c(p+'_u',0,p+'_c',0); c(p+'_c',0,p+'_inc',0); c(p+'_inc',0,p+'_c',1)
    c(p+'_c',0,p+'_get',0); c(p+'_get',0,p+'_unp',0)

# ---------- STORE <slot> ----------
X=30
o('st_t',X,130,'t b b b f')
m('st_open',X+200,180,'1'); m('st_close',X+260,180,'0')
o('st_get',X+120,230,'s \\$1-get')
o('st_slot',X+320,180,'f'); m('st_n',X+320,220,'1e+06'); o('st_u',X+320,260,'until')
o('st_f',X+320,300,'f'); o('st_s',X+320,340,f'text search {D}'); o('st_mo',X+320,380,'moses 0')
m('st_stop',X+320,420,'bang')
o('st_r',X,420,'r \\$1-collect'); o('st_g',X,460,'spigot'); o('st_sp',X,500,'list split 1')
o('st_pre',X,540,'list prepend'); o('st_app',X,580,'list append')
c('rt',0,'st_t',0)
c('st_t',3,'st_slot',0); c('st_slot',0,'st_f',1); c('st_slot',0,'st_pre',1)
c('st_slot',0,'st_n',0); c('st_n',0,'st_u',0); c('st_u',0,'st_f',0)
c('st_f',0,'st_s',0); c('st_s',0,'st_mo',0); c('st_mo',0,'st_stop',0); c('st_stop',0,'st_u',1)
c('st_mo',1,'txt',0)   # placeholder replaced below by text delete
o('st_del',X+420,420,f'text delete {D}')
conns.pop(); c('st_mo',1,'st_del',0)
c('st_t',2,'st_open',0); c('st_open',0,'st_g',1)
c('st_t',1,'st_get',0)
c('st_t',0,'st_close',0); c('st_close',0,'st_g',1)
c('st_r',0,'st_g',0); c('st_g',0,'st_sp',0); c('st_sp',1,'st_pre',0)
o('st_ins',X,620,f'text insert {D} 1e+07'); c('st_pre',0,'st_ins',0)
event('stored','st_ev',X+120,280,'st_t',0,'st_t',3)

# ---------- RECALL <slot> [ms] ----------
X=560
o('rc_app',X,130,'list append 0'); o('rc_sp',X,170,'list split 2'); o('rc_unp',X,210,'unpack f f')
o('rc_seq',X,250,'t b b b f')
m('rc_open',X+200,290,'1'); m('rc_shut',X+260,290,'0')
o('rc_ms',X+320,290,'f')
iterator('rci',X,330)
o('rc_val',X+200,620,'f'); o('rc_name',X+120,660,'symbol')
o('rc_on',X,620,'spigot'); o('rc_eq',X,660,'=='); o('rc_sel',X,700,'sel 1'); o('rc_bt',X,740,'t b b b')
o('rc_pack',X,800,'pack s f f'); o('rc_trim',X,840,'list trim'); o('rc_send',X,880,'s \\$1-set')
c('rt',1,'rc_app',0); c('rc_app',0,'rc_sp',0); c('rc_sp',0,'rc_unp',0)
c('rc_unp',1,'rc_ms',1); c('rc_unp',0,'rc_seq',0)
c('rc_seq',3,'rc_eq',1)
c('rc_seq',2,'rc_open',0); c('rc_open',0,'rc_on',1)
c('rc_seq',1,'rci_t',0)
c('rc_seq',0,'rc_shut',0); c('rc_shut',0,'rc_on',1)
c('rci_unp',2,'rc_val',1); c('rci_unp',1,'rc_name',1); c('rci_unp',0,'rc_on',0)
c('rc_on',0,'rc_eq',0); c('rc_eq',0,'rc_sel',0); c('rc_sel',0,'rc_bt',0)
c('rc_bt',2,'rc_ms',0); c('rc_ms',0,'rc_pack',2)
c('rc_bt',1,'rc_val',0); c('rc_val',0,'rc_pack',1)
c('rc_bt',0,'rc_name',0); c('rc_name',0,'rc_pack',0)
c('rc_pack',0,'rc_trim',0); c('rc_trim',0,'rc_send',0)
event('recalled','rc_ev',X+320,340,'rc_seq',0,'rc_seq',3)

# ---------- MORPH <a> <b> <t> ----------
X=1080
o('mo_unp',X,130,'unpack f f f'); o('mo_seq',X,250,'t b b b f')
m('mo_open',X+200,290,'1'); m('mo_shut',X+260,290,'0')
iterator('moi',X,330)
o('mo_val',X+200,620,'f'); o('mo_name',X+120,660,'symbol')
o('mo_on',X,620,'spigot'); o('mo_eq',X,660,'=='); o('mo_sel',X,700,'sel 1')
o('mo_key',X,740,'list prepend'); o('mo_s',X,780,f'text search {D} 0 1'); o('mo_mo',X,820,'moses 0')
o('mo_get',X+80,860,f'text get {D}'); o('mo_unp2',X+80,900,'unpack f s f')
o('mo_vt',X+80,940,'t b f'); o('mo_bt',X+80,980,'t b b')
o('mo_pack',X,1040,'pack s f f f'); o('mo_trim',X,1080,'list trim'); o('mo_send',X,1120,'s \\$1-morph')
c('rt',2,'mo_unp',0)
c('mo_unp',2,'mo_pack',3); c('mo_unp',1,'mo_key',1); c('mo_unp',0,'mo_seq',0)
c('mo_seq',3,'mo_eq',1)
c('mo_seq',2,'mo_open',0); c('mo_open',0,'mo_on',1)
c('mo_seq',1,'moi_t',0)
c('mo_seq',0,'mo_shut',0); c('mo_shut',0,'mo_on',1)
c('moi_unp',2,'mo_val',1); c('moi_unp',1,'mo_name',1); c('moi_unp',0,'mo_on',0)
c('mo_on',0,'mo_eq',0); c('mo_eq',0,'mo_sel',0)
c('mo_sel',0,'mo_name',0)
o('mo_nt',X+120,700,'t s s'); 
conns.pop(); c('mo_sel',0,'mo_name',0)
c('mo_name',0,'mo_key',0)
c('mo_key',0,'mo_s',0); c('mo_s',0,'mo_mo',0); c('mo_mo',1,'mo_get',0); c('mo_get',0,'mo_unp2',0)
c('mo_unp2',2,'mo_vt',0); c('mo_vt',1,'mo_pack',2); c('mo_vt',0,'mo_bt',0)
c('mo_bt',1,'mo_val',0); c('mo_val',0,'mo_pack',1)
o('mo_name2',X+200,1000,'symbol'); c('moi_unp',1,'mo_name2',1)
c('mo_bt',0,'mo_name2',0); c('mo_name2',0,'mo_pack',0)
c('mo_pack',0,'mo_trim',0); c('mo_trim',0,'mo_send',0)
event('morphed','mo_ev',X+320,340,'mo_seq',0,'mo_unp',2)

# ---------- WRITE / READ [file] ----------
for tag,X,sel,verb,ev in (('wr',1450,3,'write','written'),('rd',1450,4,'read','loaded')):
    Y=130 if tag=='wr' else 700
    o(tag+'_l',X,Y,'list'); o(tag+'_app',X,Y+40,'list append \\$1.stash.txt'); o(tag+'_sp',X,Y+80,'list split 1')
    o(tag+'_t',X,Y+120,'t b b l'); m(tag+'_dir',X+80,Y+160,'dir 1'); o(tag+'_pdc',X+80,Y+200,'pdcontrol')
    o(tag+'_cat',X,Y+240,'list append'); o(tag+'_join',X,Y+280,'file join')
    o(tag+'_pre',X,Y+320,'list prepend '+verb); o(tag+'_trim',X,Y+360,'list trim')
    m(tag+'_ev',X+180,Y+160,ev)
    c('rt',sel,tag+'_l',0); c(tag+'_l',0,tag+'_app',0); c(tag+'_app',0,tag+'_sp',0); c(tag+'_sp',0,tag+'_t',0)
    c(tag+'_t',2,tag+'_cat',1)
    c(tag+'_t',1,tag+'_dir',0); c(tag+'_dir',0,tag+'_pdc',0); c(tag+'_pdc',0,tag+'_cat',0)
    c(tag+'_cat',0,tag+'_join',0); c(tag+'_join',0,tag+'_pre',0); c(tag+'_pre',0,tag+'_trim',0)
    c(tag+'_trim',0,'txt',0)
    c(tag+'_t',0,tag+'_ev',0); c(tag+'_ev',0,'out',0)

m('cl',1700,520,'clear'); c('rt',5,'cl',0); c('cl',0,'txt',0)
o('note',30,1450,'stash/bank: preset manager. arg: namespace. See bank-help.pd','text')

L=["#N canvas 40 40 1900 1500 12;"]+objs+[f"#X connect {ids[a]} {ao} {ids[b]} {bi};" for a,ao,b,bi in conns]
open('abstractions/bank.pd','w').write('\n'.join(L)+'\n')
print(len(objs),len(conns))
