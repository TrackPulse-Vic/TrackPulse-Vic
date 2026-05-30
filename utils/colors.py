import discord

# Colours
achievement_colour = 0x43ea46
rare_trains_colour = 0xf23f42
ptv_grey = 0x333434

metro_colour = 0x0072ce
vline_colour = 0x8f1a95
vline_map_colour = 0x782f9a
tram_colour = 0x78be20
bus_colour = 0xff8200
coach_colour = 0xa57fb2
myki_colour = 0xc2d840

sydney_train_colour = 0xf47913
sydney_tram_colour = 0xed2438

transperth_colour = 0x008635
transwa_colour = 0xcf4520

adelaide_metro_colour = 0xf68a24 #this may or may not need fixing
adelaide_tram_colour = adelaide_metro_colour

#guesser colours
very_easy_colour = 0x89ff65
easy_colour = 0xcaff65
medium_colour = 0xffe665
hard_colour = 0xffa665
very_hard_colour = 0xff6565
ultrahard_colour = 0xe52727

def genColor(status):
    print(f"Line Status: {status}")
    if status == "Major Delays":
        return(0xef4135)
    if status == "Good Service":
        return(0x90af53)
    if status == "Minor Delays":
        return(0xe87801)
    if status == "Suspended":
        return(0x3d3d3d)
    if status == "Planned Works":
        return(0xffd500)
    
def statusEmoji(status):
    print(f"Line Status: {status}")
    if status == "Major Delays":
        return('<:majordisruptions:1267414600266289152>')
    if status == "Good Service":
        return('<:goodservice:1267414598353682463>')
    if status == "Minor Delays":
        return('<:MinorDelays:1267414596499538011>')
    if status == "Suspended" or status == 'Part Suspended':
        return('<:suspended:1267414594272362537>')
    if status == "Planned Works":
        return('<:Plannedworks:1267414592187924532>')
    if status == 'Planned Closure':
        return('🚫')
    if status == 'Timetable/Route Changes':
        return('')
    else:
        return('')

def getColor(type):
    if type == "metro" or type == "0":
        return(0x0072ce)
    if type == "tram" or type == "1":
        return(0x78be20)
    if type == "bus" or type =="2":
        return(0xff8400)
    if type == "vline" or type =="3":
        return(0x8f1a95)

def getEmojiColor(line):
    if line == "Lilydale" or line =="Belgrave" or line =="Alamein" or line =='Glen Waverley':
        return('<:burnley:1245673094509760562>')
    if line in ["Pakenham", "Cranbourne", "Sunbury"]:
        return('<:metrotunnel:1245673090495680533>')
    if line == "Hurstbridge" or line =="Mernda":
        return('<:cliftonhill:1245673092655878174>')
    if line == "Frankston" or line == 'Stony Point':
        return('<:frankston:1245673086360092735>')    
    if line == "Upfield" or line =='Craigieburn':
        return('<:northern:1245673088314638431>')    
    if line in ['Sandringham','Werribee','Williamstown']:
        return('<:crosscity:1245673084187578368>')
    if line == 'City Loop':
        return('<:cityloop:1265627754473197630>')  
    else:
        return('<:other:1245674664647331860>')
    
def getlineEmoji(type):
    if type == "Alamein":
        return('<:Alamein1:1298191533820084285><:Alamein2:1298191535854194720><:Alamein3:1298191746915893309>')
    if type == "Belgrave":
        return('<:Belgrave1:1298192329995456534><:Belgrave2:1298192428599083070><:Belgrave3:1298192440712499231>')
    if type == "Craigieburn":
        return('<:Craigieburn1:1299289280388272209><:Craigieburn2:1299289282761982032><:Craigieburn3:1299289284901081118><:Craigieburn4:1299289287782694922>')
    if type == "Cranbourne":
        return('<:Cranbourne1:1299289844131958815><:Cranbourne2:1299289846707126312><:Cranbourne3:1299289848565465160><:Cranbourne4:1299289851182714892>')
    if type == "Flemington Racecourse":
        return('<:FlemingtonRacecourse1:1299290568601636895><:FlemingtonRacecourse2:1299290570488811531><:FlemingtonRacecourse3:1299290572669849610><:FlemingtonRacecourse4:1299290574691504189><:FlemingtonRacecourse5:1299290577392766977><:FlemingtonRacecourse6:1299290580018397195><:FlemingtonRacecourse7:1299290583835213826><:FlemingtonRacecourse8:1299290585886228480>')
    if type == "Frankston":
        return('<:Frankston1:1299291143305170964><:Frankston2:1299291145355919412><:Frankston3:1299291147125915648><:Frankston4:1299291149323993168>')
    if type == "Glen Waverley":
        return('<:GlenWaverley1:1299291654364332083><:GlenWaverley2:1299291656805290025><:GlenWaverley3:1299291661867941950><:GlenWaverley4:1299291663830880287><:GlenWaverley5:1299291666490064907>')
    if type == "Hurstbridge":
        return('<:Hurstbridge1:1299603341021806604><:Hurstbridge2:1299603343358038066><:Hurstbridge3:1299603345136291850><:Hurstbridge4:1299603347556401153>')
    if type == "Lilydale":
        return('<:Lilydale1:1299603855604191344><:Lilydale2:1299603857831100487><:Lilydale3:1299603860335235082>')
    if type == "Mernda":
        return('<:Mernda1:1299604211629162556><:Mernda2:1299604213319335976><:Mernda3:1299604215282532393>')
    if type == "Pakenham":
        return('<:Pakenham1:1299604711896256544><:Pakenham2:1299604713930756137><:Pakenham3:1299604716237361182><:Pakenham4:1299604717961216073>')
    if type == "Sandringham":
        return('<:Sandringham1:1299606162647416872><:Sandringham2:1299606164471812127><:Sandringham3:1299606166598455296><:Sandringham4:1299606168464920657><:Sandringham5:1299606170733907979>')
    if type == "Stony Point":
        return('<:StonyPoint1:1299615026394431518><:StonyPoint2:1299615028659486761><:StonyPoint3:1299615030823747595><:StonyPoint4:1299615032346279989>')
    if type == "Sunbury":
        return('<:SUNBURY_1:1466034740380307528><:SUNBURY_2:1466034802493882428><:SUNBURY_3:1466034963479662677>')
    if type == "Upfield":
        return('<:Upfield1:1299615804467187762><:Upfield2:1299615806547689514><:Upfield3:1299615808896503859>')
    if type == "Werribee":
        return('<:Werribee_Pink_0_0:1466037262042009721><:Werribee_Pink_1_0:1466037295651229802><:Werribee_Pink_2_0:1466037324826808413>')
    if type == "Williamstown":
        return('<:Williamstown_Pink_0_0:1466037737093337089><:Williamstown_Pink_1_0:1466037757620129993><:Williamstown_Pink_2_0:1466037780982267934><:Williamstown_Pink_3_0:1466037806743687333><:Williamstown_Pink_4_0:1466037828596142337>')
    if type == "City Loop":
        return('<:CityCircle1:1299990618897911878><:CityCircle2:1299990620940669020><:CityCircle3:1299990622832164925><:CityCircle4:1299990625004949556>')
    else:
        return type
    
def getMapEmoji(line, type):
    if line == "Lilydale" or line =="Belgrave" or line =="Alamein" or line =='Glen Waverley':
        if type == "terminus":
            return('<:bt:1319982837348438067>')
        if type == "terminus2":
            return('<:bt2:1320227114879946833>')
        if type == "stop":
            return('<:bst:1319980922497536040>')
        if type == "interchange":
            return('<:bi:1320141641650016337>')
        if type == "cont1":
            return('<:bbr:1320142969860263976>')
        if type == "cont2":
            return('<:bbr2:1320142972171587746>')
        if type == 'skipped':
            return('<:be:1322709966758350848>')
        if type == 'interchange_first':
            return('<:bit:1322897569042399243>')
        if type == 'interchange_last':
            return('<:bit2:1322897579683479576>')
        else:
            return '⚠'
        
    if line == "Pakenham" or line =="Cranbourne" or line =="Sunbury":
        if type == "terminus":
            return('<:dt:1319982841580224572>')
        if type == "terminus2":
            return('<:dt2:1320227120307507330>')
        if type == "stop":
            return('<:dst:1319980927988006958>')
        if type == "interchange":
            return('<:ci:1320142974306484244>')
        if type == "cont1":
            return('<:dbr:1320145219978530919>')
        if type == "cont2":
            return('<:dbr2:1320145221698195556>')
        if type == 'skipped':
            return('<:de:1322710023268339774>')
        if type == 'interchange_first':
            return('<:dit:1322897682561372242>')
        if type == 'interchange_last':
            return('<:dit2:1322897692258467891>')
        else:
            return '⚠'
        
    if line == "Stony Point":
        if type == "terminus":
            return('<:st:1320631767904030791>')
        if type == "terminus2":
            return('<:st2:1320631769656987658>')
        if type == "stop":
            return('<:sst:1320631765567799337>')
        if type == "interchange":
            return('<:si:1320142987388391537>')
        if type == "cont1":
            return('<:stbr:1320631771406274671>')
        if type == "cont2":
            return('<:stbr2:1320631773209690194>')
        if type == 'skipped':
            return('<:ste:1322710199437365298>')
        if type == 'interchange_first':
            return('<:stit:1322897817332617366>')
        if type == 'interchange_last':
            return('<:stit2:1322897830788206592>')
        else:
            return '⚠'
        
    if line == "Frankston":
        if type == "terminus":
            return('<:ft:1319982844533280831>')
        if type == "terminus2":
            return('<:ft2:1320227124099022918>')
        if type == "stop":
            return('<:fst:1319980930722435082>')
        if type == "interchange":
            return('<:fi:1320142976013307946>')
        if type == "cont1":
            return('<:fbr:1320145223493353566>')
        if type == "cont2":
            return('<:fbr2:1320145225527722015>')
        if type == 'skipped':
            return('<:fe:1322710042230653009>')
        if type == 'interchange_first':
            return('<:fit:1322897707483791451>')
        if type == 'interchange_last':
            return('<:fit2:1322897720624807986>')
        else:
            return '⚠'
        
    if line == "Sandringham" or line =="Werribee" or line =="Williamstown":
        if type == "terminus":
            return('<:crt:1319982839701180436>')
        if type == "terminus2":
            return('<:crt2:1320227116654264391>')
        if type == "stop":
            return('<:csst:1319980924775170178>')
        if type == "interchange":
            return('<:sant:1320142985198829620>')
        if type == "cont1":
            return('<:csbr:1320145216149258364>')
        if type == "cont2":
            return('<:csbr2:1320145218200404018>')
        if type == 'skipped':
            return('<:cse:1322709995078287482>')
        if type == 'interchange_first':
            return('<:crit:1322897623962878052>')
        if type == 'interchange_last':
            return('<:crit2:1322897635664855104>')
        else:
            return '⚠'
    
    if line == "Upfield" or line =="Craigieburn":
        if type == "terminus":
            return('<:nt:1320523324308197397>')
        if type == "terminus2":
            return('<:nt2:1320523326153687061>')
        if type == "stop":
            return('<:nst:1320523322311573585>')
        if type == "interchange":
            return('<:ni:1320142983722434583>')
        if type == "cont1":
            return('<:nbr:1320145231290695680>')
        if type == "cont2":
            return('<:nbr2:1320145280569442426>')
        if type == 'skipped':
            return('<:ne:1322710100061847636>')
        if type == 'interchange_first':
            return('<:nit:1322897779131023462>')
        if type == 'interchange_last':
            return('<:nit2:1322897794184515615>')
        else:
            return '⚠'
        
    if line == "Mernda" or line =="Hurstbridge":
        if type == "terminus":
            return('<:ct:1319982465594429442>')
        if type == "terminus2":
            return('<:ct2:1320227118491373609>')
        if type == "stop":
            return('<:cst:1319980926440312884>')
        if type == "interchange":
            return('<:chi:1320148570925564046>')
        if type == "cont1":
            return('<:cbr:1320145212823175189>')
        if type == "cont2":
            return('<:cbr2:1320145214467215411>')
        if type == 'skipped':
            return('<:ce:1322709978859180053>')
        if type == 'interchange_first':
            return('<:cit:1322897599937642596>')
        if type == 'interchange_last':
            return('<:cit2:1322897612159979542>')
        else:
            return '⚠'
        
    if line == "Flemington Racecourse":
        if type == "terminus":
            return('<:frt:1322903781842616411>')
        if type == "terminus2":
            return('<:frt2:1322903791523332148>')
        if type == "stop":
            return('<:frs:1322903770073530449>')
        if type == "interchange":
            return('<:fri:1322903741422108786>')
        if type == "cont1":
            return('<:frbr:1322903633892868127>')
        if type == "cont2":
            return('<:frbr2:1322903649290289245>')
        if type == 'skipped':
            return('<:fre:1322903729959211143>')
        if type == 'interchange_first':
            return('<:frit:1322897739062706236>')
        if type == 'interchange_last':
            return('<:frit2:1322897752191008839>')
        else:
            return '⚠'
        
    if line == "V/Line":
        if type == "terminus":
            return('<:vt:1322740727729487944>')
        if type == "terminus2":
            return('<:vt2:1322740741126099006>')
        if type == "stop":
            return('<:vst:1322740715125735454>')
        if type == "interchange":
            return('<:vi:1322740701514960996>')
        if type == "cont1":
            return('<:vbr:1322740666429603860>')
        if type == "cont2":
            return('<:vbr2:1322740683773055046>')
        if type == 'skipped':
            return('<:ve:1322740553758150666>')
        if type == 'interchange_first':
            return('<:vit:1322740867869708329>')
        if type == 'interchange_last':
            return('<:vit2:1322740857685803060>')
        else:
            return '⚠'
    
    if line == "bus" or line =="tram":
        if type == "terminus":
            return('<:frt:1322903781842616411>')
        if type == "terminus2":
            return('<:frt2:1322903791523332148>')
        if type == "stop":
            return('<:frs:1322903770073530449>')
        if type == "interchange":
            return('<:fri:1322903741422108786>')
        if type == "cont1":
            return('<:frbr:1322903633892868127>')
        if type == "cont2":
            return('<:frbr2:1322903649290289245>')
        if type == 'skipped':
            return('<:fre:1322903729959211143>')
        if type == 'interchange_first':
            return('<:frit:1322897739062706236>')
        if type == 'interchange_last':
            return('<:frit2:1322897752191008839>')
        else:
            return '⚠'
    
    else:
        if type == "terminus":
            return('<:ot:1325248217599705118>')
        if type == "terminus2":
            return('<:ot2:1325248229419258018>')
        if type == "stop":
            return('<:ost:1325248202537963631>')
        if type == "interchange":
            return('<:oi:1325248161815462048>')
        if type == "cont1":
            return('<:obr:1325248124125446265>')
        if type == "cont2":
            return('<:obr2:1325248137144827995>')
        if type == 'skipped':
            return('<:oe:1325248147467010070>')
        if type == 'interchange_first':
            return('<:oit:1325248174675198104>')
        if type == 'interchange_last':
            return('<:oit2:1325248188709343293>')
        else:
            return '⚠'
    
def getEmojiForDeparture(trainType):
    if trainType == "6 Car Comeng":
        return('<:edi:1325040436946931754> x6')
    elif trainType == "3 Car Comeng":
        return('<:edi:1325040436946931754> x3')
    elif trainType == "6 Car Siemens":
        return('<:siemens:1325040408866193449> x6')
    elif trainType == "3 Car Siemens":
        return('<:siemens:1325040408866193449> x3')  
    elif trainType == "6 Car Xtrapolis":
        return('<:xtrap:1325040397688377364> x6')
    elif trainType == "3 Car Xtrapolis":
        return('<:xtrap:1325040397688377364> x3') 
    elif trainType == "7-car HCMT":
        return('<:hcmt:1325040456496713768> x7')
    elif trainType == "Sprinter":
        return('<:sprinter:1325040386913075200>')
    else:
        return(trainType)
    
def getTrainTypeEmoji(trainType):
    if trainType == "Comeng":
        return('<:EDIComeng:1214140064653639712> <:AlstomComeng:1214140062187388968>')
    elif trainType == "Siemens Nexas":
        return('<:siemens:1325040408866193449>')
    elif trainType == "X'Trapolis 100":
        return('<:xtrap:1325040397688377364>')
    elif trainType == "HCMT":
        return('<:hcmt:1325040456496713768>')
    elif trainType == "Sprinter":
        return('<:sprinter:1325040386913075200>')
    elif trainType == "VLocity":
        return('<:VLocity:1214140045133348906>')
    elif trainType == 'N Class':
        return('<:NClass:1214140049243770911>')
    else:
        return('')

def getModeEmoji(mode:int):
    if mode == 0:
        return('<:train:1241164967789727744>')
    if mode == 1:
        return('<:tram:1241165701390012476>')
    if mode == 2:
        return('<:bus:1241165769241530460>')
    if mode == 3:
        return('<:vline:1241165814258729092>')
    
def yesOrNo(input:bool):
    if input:
        return('✅')
    else:
        return('❌')
    
def getSydneyTrainIcon(train:str, discord_format:bool=True):
    if discord_format:
        if train == 'Waratah A set' or train == 'Waratah B set':
            file = discord.File("assets/nsw-train-icons/waratah.jpg", filename="image.png")
        elif train == 'OSCar':
            file = discord.File("assets/nsw-train-icons/Oscar.jpg", filename="image.png")
        elif train == 'Hunter':
            file = discord.File("assets/nsw-train-icons/Hunter.jpg", filename="image.png")
        elif train == 'K Set':
            file = discord.File("assets/nsw-train-icons/K-Set.jpg", filename="image.png")
        elif train == 'Millenium':
            file = discord.File("assets/nsw-train-icons/Millenium.jpg", filename="image.png")
        elif train == 'Endeavour':
            file = discord.File("assets/nsw-train-icons/Endeavour.jpg", filename="image.png")
        elif train == 'Tangara':
            file = discord.File("assets/nsw-train-icons/Tangara.jpg", filename="image.png")
        elif train == 'V Set':
            file = discord.File("assets/nsw-train-icons/Vset.jpg", filename="image.png")
        else:
            file = None
        return file        