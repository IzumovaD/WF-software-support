#массив корневых алломорфов: каждый элемент - группа алломорфных корней
root_allomorphs = [["дукт", "дукц", "дуц"],
                   ["абстракт", "абстракц"],
                   ["автомобиль", "автомобил"],
                   ["министр", "министер"],
                   ["акварель", "акварел"],
                   ["акт", "акц"],
                   ["алле", "аллей"],
                   ["мораль", "морал"],
                   ["анализ", "аналит"],
                   ["ангел", "ангель"],
                   ["антенн", "антен"],
                   ["бактерий", "бактери"],
                   ["вещ", "вест"],
                   ["совет", "совещ"],
                   ["плик", "плиц"],
                   ["аптек", "аптеч"],
                   ["ари", "арий"],
                   ["арифметик", "арифметичн"],
                   ["артель", "артел"],
                   ["тем", "тм", "темн", "тмен", "темен", "тьм"],
                   ["бак", "бач"],
                   ["бакале", "бакалей"],
                   ["балала", "балалай"],
                   ["ответ", "отвеч"],
                   ["баламут", "баламуч"],
                   ["бандероль", "бандерол"],
                   ["бан", "бань"],
                   ["баран", "бараш"],
                   ["барсук", "барсуч"],
                   ["бархат", "бархот"],
                   ["батаре", "батарей"],
                   ["батрак", "батрач", "батрац"],
                   ["хвал", "хваль"],
                   ["башн", "башен"],
                   ["бег", "беж", "бегл"],
                   ["бедр", "бедер"],
                   ["бед", "бежд"],
                   ["бок", "боч"],
                   ["боль", "бол", "бал"],
                   ["берег", "бреж", "береж", "бере"],
                   ["верх", "верш"],
                   ["ветер", "ветр"],
                   ["кус", "куш"],
                   ["дар", "дарь"],
                   ["дей", "де"],
                   ["дел", "дель"],
                   ["душ", "дух"],
                   ["завет", "завещ"],
                   ["щит", "щищ"],
                   ["звук", "звуч"],
                   ["лиц", "лик", "личн", "лич"],
                   ["мер", "мир"],
                   ["зор", "зр", "зир", "зар"],
                   ["обид", "обиж"],
                   ["облач", "оболоч", "облак"],
                   ["образ", "ображ"],
                   ["гляд", "глян", "гля"],
                   ["чет", "чит", "чт", "чес", "чеш", "чт"],
                   ["ум", "умл"],
                   ["язык", "языч"],
                   ["им", "ым", "имен", "ымен"],
                   ["бел", "бель"],
                   ["бенефис", "бенефит", "бенефиц"],
                   ["бес", "беш"],
                   ["корм", "кармл", "кормл"],
                   ["бой", "бое", "бо", "ба"],
                   ["печ", "пек", "пе"],
                   ["покой", "поко"],
                   ["буд", "бужд", "буж"],
                   ["игр", "игор", "ыгр"],
                   ["путь", "пут"],
                   ["сердц", "сердеч"],
                   ["структ", "струкц"],
                   ["талант", "талан"],
                   ["фамил", "фамиль"],
                   ["форм", "формл"],
                   ["библиотек", "библиотеч"],
                   ["бив", "бивн", "би", "бит", "бь"],
                   ["благ", "блаж", "блажь"],
                   ["блест", "блес", "блеск"],
                   ["близ", "ближ"],
                   ["леж", "лег", "ле"],
                   ["блок", "блоч"],
                   ["блуд", "блужд"],
                   ["блюд", "блюс", "блюст"],
                   ["бобр", "бобер"],
                   ["бог", "бож"],
                   ["бод", "бодл"],
                   ["бодр", "бадр"],
                   ["бокал", "бокаль"],
                   ["болот", "болач", "болоч"],
                   ["болт", "балт"],
                   ["брак", "брач"],
                   ["бр", "бир", "бри", "брит", "бре","бор", "бер", "борь"],
                   ["брод", "бред", "брес"],
                   ["бриллиант", "брильянт"],
                   ["бров", "бровь"],
                   ["брос", "брош", "брас", "брошь"],
                   ["брусник", "бруснич"],
                   ["брюзг", "брюзж"],
                   ["брюк", "брюч"],
                   ["брюх", "брюш"],
                   ["бугор", "бугр"],
                   ["буй", "бу"],
                   ["букв", "буков"],
                   ["бумаг", "бумаж"],
                   ["бур", "бурл"],
                   ["бурлак", "бурлач"],
                   ["бутыл", "бутыль", "бутил"],
                   ["бутон", "бутонь"],
                   ["бух", "бухл"],
                   ["быв", "был", "быт", "быч", "бык", "бы", "бв", "быль"],
                   ["быстр", "бистр"],
                   ["бюрократ", "бюрокрач"],
                   ["вал", "валь"],
                   ["ваниль", "ванил"],
                   ["воз", "вез"],
                   ["век", "веч"],
                   ["верт", "верч"],
                   ["вес", "веш", "вис", "вс"],
                   ["вод", "вож", "вожд", "важ"],
                   ["гон", "гн", "гно", "гни", "гнил", "гной", "гниль"],
                   ["да", "дав", "дан", "дат", "давл", "дач"],
                   ["долб", "далбл", "долбл"],
                   ["двиг", "дви", "двин", "движ"],
                   ["де", "дев", "дет"],
                   ["дыш", "дых", "дох", "дош"],
                   ["ду", "дув", "дут"],
                   ["ведр", "ведер"],
                   ["велич", "велик"],
                   ["венгр", "венгер"],
                   ["вентил", "вентиль"],
                   ["венец", "венч"],
                   ["верблюд", "верблюж"],
                   ["вертикал", "вертикаль"],
                   ["весел", "весл"],
                   ["весн", "весен"],
                   ["ветв", "вет", "ветвл"],
                   ["ветх", "ветш"],
                   ["жат", "жав", "жим", "жа"],
                   ["жив", "живл", "жиз", "жит", "жил", "жиль", "жи", "жизн"],
                   ["гром", "громл"],
                   ["лом", "лам", "ломл"],
                   ["мах", "маш"],
                   ["моч", "мок", "мач", "мк", "мык", "мат", "мот"],
                   ["мы", "мыв", "мыт", "мой", "мо"],
                   ["нос", "нош", "нес", "наш"],
                   ["ид", "й"],
                   ["рв", "рыв", "ров", "рыт"],
                   ["рас", "ращ", "рос", "росл", "рост"],
                   ["рез", "реж", "резь", "ред"],
                   ["зв", "зыв", "зов"],
                   ["иск", "ыск", "ищ", "ист"],
                   ["вил", "виль"],
                   ["винт", "винч"],
                   ["вихр", "вихор"],
                   ["кол", "кал", "коль"],
                   ["коп", "кап"],
                   ["кат", "кач"],
                   ["краж", "крад", "крас"],
                   ["крут", "круч"],
                   ["ли", "лив", "лит", "ливн"],
                   ["лож", "лог", "лг", "лаг", "лж"],
                   ["люб", "любл"],
                   ["маз", "маж"],
                   ["мороз", "мерз", "мораж", "мерзл", "морож"],
                   ["мест", "мещ", "мщ"],
                   ["меш", "мес", "мех", "мет", "меч", "метл"],
                   ["черед", "чрежд"],
                   ["ник", "ниц"],
                   ["ним", "нят", "ят", "яз", "н", "я"],
                   ["внук", "внуч"],
                   ["влек", "влеч", "вле"],
                   ["ворот", "врат", "вращ"],
                   ["выс", "выш"],
                   ["голов", "глав", "главл"],
                   ["мут", "мущ"],
                   ["нов", "новл"],
                   ["раз", "раж"],
                   ["вол", "воль", "вел"],
                   ["волок", "волоч"],
                   ["низ", "ниж", "нз"],
                   ["оруж", "оруд"],
                   ["прос", "прош", "прось", "праш"],
                   ["воскрес", "воскреш"],             
                   ["паль", "пал"],
                   ["пит", "пи", "пить", "пь", "пив", "пищ", "писк"],
                   ["прещ", "прет"],
                   ["ста", "став", "ставл", "cто", "стан", "стой", "сто"],
                   ["торг", "торж"],
                   ["хит", "хищ"],
                   ["ход", "хожд", "хож", "хаж"],
                   ["шед", "шл"],
                   ["пав", "пал", "пад", "пас", "пасл"],
                   ["пир", "пер", "пар", "пор"],
                   ["пис", "пиш", "письм"],
                   ["плы", "плыв"],
                   ["прав", "правл", "правд", "правед"],
                   ["прыг", "прыж", "пры"],
                   ["прям", "прямл"],
                   ["пуск", "пущ", "пуст"],
                   ["враг", "враж", "вражд"],
                   ["вред", "врежд"],
                   ["руб", "рубл"],
                   ["руч", "рук"],
                   ["сос", "сас"],
                   ["крыв", "крыт", "кры", "крыш"],
                   ["слуш", "слух", "слыш", "слых", "слушл"],
                   ["смотр", "сматр"],
                   ["сох", "сых", "суш", "сух"],
                   ["пах", "паш"],
                   ["плак", "плач", "плат"],
                   ["помин", "помн"],
                   ["пух", "пуш", "пухл"],
                   ["пыль", "пыл"],
                   ["стра", "стро", "строй"],
                   ["трях", "тряс"],
                   ["ступ", "ступл"],
                   ["сп", "сып", "сн", "сон", "сыпл"],
                   ["толк", "талк", "толч"],
                   ["тер", "тр", "тир"],
                   ["трав", "травл"],
                   ["тык", "тыч"],
                   ["тяг", "тяж", "тян", "тягл", "тя"],
                   ["ши", "шив", "шит", "шь", "шв", "шве", "шов"],
                   ["ед", "ес"],
                   ["езд", "ех", "езж"],
                   ["глаж", "глад"],
                   ["говар", "говор", "говорл"],
                   ["год", "годл", "гожд"],
                   ["гораж", "город", "горож", "град", "гражд"],
                   ["гор", "гар"],
                   ["груз", "груж"],
                   ["гул", "гуль"],
                   ["жд", "жид"],
                   ["жиг", "жег", "жж"],
                   ["жир", "жр", "жор"],
                   ["здоравл", "здоровл", "здрав", "здоров"],
                   ["каз", "каж"],
                   ["краш", "крас"],
                   ["крест", "крещ"],
                   ["кро", "крой"],
                   ["куп", "купл"],
                   ["молач", "молот", "молоть", "молок", "молоч"],
                   ["мысл", "мысел", "мышл"],
                   ["нужд", "нуд", "нуж"],
                   ["плав", "плавл"],
                   ["прост", "прощ", "пращ", "праст"],
                   ["рабат", "работ", "рабоч"],
                   ["равн", "ровн"],
                   ["род", "рожд"],
                   ["ряд", "ряж"],
                   ["сад", "саж", "сид", "сажд", "сед", "сес", "сиж", "садл", "садн"],
                   ["свет", "свеч", "светл", "свещ"],
                   ["свобод", "свобожд"],
                   ["сек", "сеч", "секц", "сект", "се"],
                   ["скаж", "сказ"],
                   ["сыл", "сл", "сол", "соль"],
                   ["след", "слеж"],
                   ["слуг", "служ", "служл"],
                   ["смех", "сме", "смешл", "смеш", "см"],
                   ["стел", "стил", "стл", "стиль"],
                   ["страд", "стражд"],
                   ["стрел", "стрель"],
                   ["студ", "стуж"],
                   ["топл", "тапл", "топ", "тепл"],
                   ["таск", "тащ"],
                   ["тач", "точ"],
                   ["тек", "теч", "ток", "точ"],
                   ["уч", "ук", "ущ"],
                   ["хват", "хвач"],
                   ["хлоп", "хлап"],
                   ["холаж", "холож", "хлажд", "хлад", "холод"],
                   ["цвет", "цвес"],
                   ["чист", "чищ"],
                   ["вяж", "вяз"],
                   ["гад", "гаж", "гадл"],
                   ["гармон", "гармош"],
                   ["гас", "гаш"],
                   ["геро", "герой", "герои"],
                   ["гибель", "гибел", "гиб", "гибл"],
                   ["гипотез", "гипотет"],
                   ["глас", "голос", "глаш"],
                   ["глот", "глощ", "глат", "глоч"],
                   ["глох", "глуш", "глух"],
                   ["глуб", "глубл"],
                   ["глуп", "глупл"],
                   ["гнев", "гневл"],
                   ["гореч", "горч", "горкл", "горьк", "горк"],
                   ["готов", "готовл", "готавл"],
                   ["греб", "гребл"],
                   ["грек", "греч", "грец"],
                   ["грех", "греш"],
                   ["гроз", "грож"],
                   ["грыз", "грызл", "грыж"],
                   ["дал", "даль"],
                   ["дво", "двой", "дву", "два"],
                   ["двулик", "двулич"],
                   ["квалифик", "квалифиц"],
                   ["дерев", "древ", "дров"],
                   ["детал", "деталь"],
                   ["диагонал", "диагональ"],
                   ["див", "дивл"],
                   ["дик", "дич"],
                   ["дикт", "дикц"],
                   ["директ", "дирекц"],
                   ["крет", "крец"],
                   ["дл", "доль"],
                   ["дн", "дон"],
                   ["бав", "бавл"],
                   ["добр", "дабр"],
                   ["дожд", "дождл"],
                   ["до", "дой"],
                   ["конч", "канч", "конеч", "конц", "конец"],
                   ["крик", "крич"],
                   ["долг", "долж", "далж"],
                   ["ныне", "нынче"],
                   ["дорог", "дорож", "драж"],
                   ["спев", "спе", "спеш", "спех"],
                   ["стиг", "сти", "стиж"],
                   ["досуг", "досуж"],
                   ["дрем", "дремл"],
                   ["дроб", "дробл"],
                   ["друг", "друж", "друз"],
                   ["дуб", "дубл", "дупл"],
                   ["дым", "дымл"],
                   ["един", "один"],
                   ["жул", "жуль"],
                   ["журнал", "журналь"],
                   ["дир", "др", "дер"],
                   ["ем", "йм", "емл"],
                   ["земель", "земл", "зем"],
                   ["кид", "кин"],
                   ["кля", "клят", "клятв"],
                   ["кольц", "кольч"],
                   ["комплект", "комплекц"],
                   ["конверт", "конверс"],
                   ["корен", "кореш", "корн"],
                   ["корот", "крат", "кращ", "корач", "короч", "кратч"],
                   ["кра", "край"],
                   ["креп", "крепл", "крепч"],
                   ["круг", "кругл", "круж"],
                   ["лад", "лаж"],
                   ["малч", "молч", "малк", "молк"],
                   ["модул", "модуль"],
                   ["мя", "мят", "мн"],
                   ["па", "паек", "пай"],
                   ["печат", "печатл"],
                   ["плет", "плеч"],
                   ["плющ", "плюс"],
                   ["предел", "предель"],
                   ["решет", "решеч"],
                   ["сал", "саль"],
                   ["секрет", "секреч"],
                   ["сил", "силь"],
                   ["снег", "снеж"],
                   ["стекл", "стеколь"],
                   ["столб", "столбл"],
                   ["стол", "столь"],
                   ["страх", "страш"],
                   ["строк", "строч"],
                   ["стру", "струй"],
                   ["стук", "стуч"],
                   ["суд", "суж", "сужд","судь"],
                   ["та", "таин", "тай"],
                   ["тверд", "твержд"],
                   ["трат", "трач"],
                   ["треб", "требл"],
                   ["треп", "трепл"],
                   ["труд", "труж", "тружд"],
                   ["туп", "тупл"],
                   ["тух", "туш", "тухл"],
                   ["ух", "уш"],
                   ["хорон", "хран"],
                   ["цеп", "цепл"],
                   ["част", "частл", "чащ"],
                   ["шум", "шумл"],
                   ["яв", "явл"],
                   ["зерк", "зерц"],
                   ["зме", "змей"],
                   ["знак", "знач"],
                   ["золот", "золоч"],
                   ["идеал", "идеаль"],
                   ["леч", "лек"],
                   ["лиш", "лих"],
                   ["лук", "луч"],
                   ["мельч", "мелк", "мелоч"],
                   ["мук", "муч"],
                   ["обрес", "обрет"],
                   ["рек", "реч", "риц"],
                   ["язв", "язвл"],
                   ["индивидуал", "индивидуаль"],
                   ["индикат", "индикац"],
                   ["инквизит", "инквизиц"],
                   ["спект", "спекц"],
                   ["интриг", "интриж"],
                   ["порт", "порч"],
                   ["том", "томл"],
                   ["итог", "ытож"],
                   ["казак", "казач"],
                   ["канал", "каналь"],
                   ["капитал", "капиталь"],
                   ["кос", "кас", "кось", "кош"],
                   ["клан", "клон"],
                   ["книг", "книж"],
                   ["ковер", "ковр"],
                   ["коллект", "коллекц"],
                   ["коллег", "коллеж"],
                   ["колодез", "колод", "колодц"],
                   ["комик", "комич"],
                   ["коммуник", "коммуниц"],
                   ["консал", "консул", "консуль"],
                   ["коре", "корей"],
                   ["коррект", "коррекц"],
                   ["кост", "костл"],
                   ["котел", "котл"],
                   ["крапл", "крап"],
                   ["кристаль", "кристалл"],
                   ["критик", "критич"],
                   ["крох", "крош"],
                   ["круп", "крупн"],
                   ["крюк", "крюч"],
                   ["кулак", "кулач", "кулачь"],
                   ["легк", "легч"],
                   ["лед", "льд"],
                   ["лест", "льст"],
                   ["магистр", "магистер"],
                   ["магнит", "магнич"],
                   ["мал", "маль"],
                   ["мебель", "мебел"],
                   ["медал", "медаль"],
                   ["мелколист", "мелколиств"],
                   ["мертв", "мерт"],
                   ["мил", "миль"],
                   ["могил", "могиль"],
                   ["модел", "модель"],
                   ["мозг", "мозгл"],
                   ["мозол", "мозоль"],
                   ["молод", "молож"],
                   ["монарх", "монарш"],
                   ["монаш", "монаст"],
                   ["мох", "мш"],
                   ["мрак", "мрач", "мерк", "мереч"],
                   ["мыл", "мыль"],
                   ["мышьяк", "мышьяч"],
                   ["мяг", "мягч", "мяк", "мягк"],
                   ["навет", "навещ"],
                   ["пол", "поль"],
                   ["рух", "руш"],
                   ["слад", "слажд", "слащ", "сласт"],
                   ["смол", "смоль"],
                   ["строж", "строг"],
                   ["сыт", "сыщ"],
                   ["хам", "хамл"],
                   ["цел", "цель"],
                   ["веж", "вежд"],
                   ["реал", "реаль"],
                   ["свой", "сво", "сва"],
                   ["соб", "собл"],
                   ["способ", "способл"],
                   ["счастл", "счаст"],
                   ["трезв", "трезвл"],
                   ["чувств", "чувствл"],
                   ["шут", "шутл"],
                   ["ног", "нож"],
                   ["ногот", "ногт"],
                   ["номер", "нумер"],
                   ["ноч", "нощ"],
                   ["оберн", "оборач", "оборот", "обрат", "обращ"],
                   ["особл", "особ"],
                   ["угл", "уголь", "угол"],
                   ["уз", "уж"],
                   ["славл", "словл", "слов"],
                   ["объем", "объемл"],
                   ["овес", "овс"],
                   ["огн", "огон", "огонь"],
                   ["пазд", "позд"],
                   ["опи", "опий", "опиум"],
                   ["сред", "серед"],
                   ["публик", "публиц", "публич"],
                   ["оригинал", "оригиналь"],
                   ["рог", "рож"],
                   ["свят", "свящ"],
                   ["скорб", "скорбл"],
                   ["слаб", "слабл"],
                   ["слеп", "слепл"],
                   ["смысл", "смышл"],
                   ["стал", "сталь"],
                   ["стбл", "стебель"],
                   ["отеч", "отц", "отч", "отец"],
                   ["редакт", "редакц"],
                   ["стран", "сторон"],
                   ["сут", "сущ"],
                   ["чуж", "чужд"],
                   ["шелом", "шеломл"],
                   ["паралит", "парализ", "паралич"],
                   ["патриарх", "патриарш"],
                   ["пред", "прежд"],
                   ["пес", "пс"],
                   ["песоч", "песок", "песч"],
                   ["плод", "плож"],
                   ["плоск", "площ"],
                   ["плот", "плоч"],
                   ["подобл", "подоб"],
                   ["ствол", "стволь"],
                   ["танц", "танец"],
                   ["политик", "политич"],
                   ["полотен", "полотн"],
                   ["привет", "привеч"],
                   ["порог", "порож"],
                   ["сло", "слой"],
                   ["срам", "срамл"],
                   ["тех", "теш"],
                   ["треск", "тресн"],
                   ["хорош", "хораш"],
                   ["практик", "практиц", "практич"],
                   ["убежд", "убед"],
                   ["претенд", "претенз", "претенц"],
                   ["стыд", "стыж"],
                   ["провок", "провоц"],
                   ["проект", "проекц", "проец"],
                   ["репетиц", "репетит"],
                   ["протект", "протекц"],
                   ["против", "противл"],
                   ["птиц", "птич"],
                   ["регулир", "регуляр", "регулят", "регуляц"],
                   ["резидент", "резиденц"],
                   ["рефлекс", "рефлект"],
                   ["фракт", "фракц"],
                   ["рецепц", "рецепт"],
                   ["самоуправ", "самоуправл"],
                   ["свекл", "свеколь"],
                   ["свист", "свищ"],
                   ["семей", "семь"],
                   ["сепарат", "сепарац"],
                   ["скаль", "скал"],
                   ["скандал", "скандаль"],
                   ["скепс", "скепт"],
                   ["созд", "созид"],
                   ["суч", "сук"],
                   ["стабил", "стабиль"],
                   ["стерил", "стериль"],
                   ["стрем", "стремл"],
                   ["тро", "треш", "трой", "трет"],
                   ["стул", "стуль"],
                   ["сумереч", "сумрач", "сумерк", "сумрак"],
                   ["табак", "табач"],
                   ["табел", "табл"],
                   ["текстил", "текстиль"],
                   ["тотал", "тоталь"],
                   ["траль", "траул"],
                   ["тыл", "тыль"],
                   ["узел", "узл"],
                   ["урок", "уроч"],
                   ["щербл", "щерб"],
                   ["хлебопах", "хлебопаш"],
                   ["целлул", "целлюл"],
                   ["цивил", "цивиль"],
                   ["черкес", "черкеш"],
                   ["черт", "черч"],
                   ["школ", "школь"],
                   ["этик", "этич"],
                   ["ядер", "ядр"],
                   ["яич", "яйц"],
                   ["ярк", "яр"]
    ]
