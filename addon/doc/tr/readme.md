# NVDA Geliştirici ve Test Araç Kutusu

* Yazar: Cyrille Bougot
* NVDA uyumluluğu: 2019.2 ve sonrası

NVDA Geliştirici ve Test Araç Kutusu, NVDA'yı hata ayıklama ve test etme araçları sağlar.
Günlük kayıt araçları, günlük kayıtlarında gezinmeyi ve analiz etmeyi, hataları ve izleme kayıtlarını incelemeyi, günlük yedeklerini kaydetmeyi ve paylaşmadan önce günlükleri anonimleştirmeyi kolaylaştırır.
Belirli fonksiyon çağrıları ve işaretleyiciler de kaydedilebilir.
Ayrıca, log kayıtlarından, konsol değişkenlerinden veya hatta bir komut yazma hareketinden ilgili kaynak kodu açmak da mümkündür.
Bu eklenti ayrıca Python konsolunu genişletir ve NVDA'nın arayüz dizelerinin ters çevirisi ve geliştirilmiş bir yeniden başlatma iletişim kutusu gibi yardımcı programlar sağlar.

## Özellikler

* NVDA'yı yeniden başlatırken bazı ek seçenekleri belirtmek için geliştirilmiş bir yeniden başlatma iletişim kutusu.
* Kaydedilen hatalarla ilgili çeşitli özellikler.
* Nesne özelliklerini inceleyen bir araç.
* Komut dosyası ve kaynak kod araçları: genişletilmiş komut dosyası açıklama modu ve kaynak kod açma komutları.
* Günlük kayıtlarını okumaya ve analiz etmeye yardımcı olacak komutlar.
* Eski günlüklerin yedekleri
* Bir günlük kaydını anonimleştirmek için kullanılan komut
* Python konsoluna özel bir başlangıç ​​komut dosyası ve NVDA yeniden başlatıldıktan sonra giriş geçmişini bellekte saklama olanağı gibi geliştirmeler eklendi.
* Python konsol çalışma alanında, bir nesnenin kaynak kodunu açmak için kullanılan bir fonksiyon.
* Belirli bir fonksiyonun (örneğin `speech.speech.speak`) çağrılarını, hata izleme kaydı da dahil olmak üzere kaydetmek için kullanılan bir komut.
* Arayüzdeki çevirileri tersine çevirmek için kullanılan bir komut.

## Komutlar

Bu eklenti, eklediği tüm yeni komutlar için katman komutları kullanır.
Bu komutların giriş noktası `NVDA+Z`'dir; bu nedenle tüm komutlar `NVDA+Z` tuş kombinasyonunun ardından tek bir harf veya hareketle yürütülmelidir.
Gerekirse, Girdi hareketleri iletişim kutusunda bunu değiştirebilirsiniz.

Bu dokümantasyonun geri kalanında, bu harekete `NDTTGesture` olarak atıfta bulunacağız.
Örneğin, `NDTTGesture, S` ifadesi, varsayılan hareketi değiştirmediğiniz sürece `NVDA+Z, S` anlamına gelir.

`NDTTGesture, H` tuşlarına basarak mevcut tüm katman komutlarını listeleyebilirsiniz.

Daha sık kullandığınız komutlar için, girdi hareketi iletişim kutusunda doğrudan bir hareket de tanımlayabilirsiniz.

## Gelişmiş yeniden başlatma iletişim kutusu

`NDTTGesture, Q` komutu, NVDA'yı yeniden başlatmadan önce bazı ek seçenekleri belirtmek için bir iletişim kutusu açar.
Belirtilebilecek seçenekler, `nvda.exe` ile kullanılabilen [komut satırı seçeneklerine][2] karşılık gelir; örneğin, yapılandırma yolu için `-c`, eklentileri devre dışı bırakmak için `--disable-addons`, vb.

## Kaydedilen hatalarla ilgili özellikler

### Son kaydedilen hatayı bildir

`NDTTGesture, E` tuşlarına basmak, log dosyasını açmaya gerek kalmadan en son kaydedilen hatayı bildirmenizi sağlar.
İkinci bir basış, hafızaya alınmış son hatayı siler.

### Kaydedilen hatalar için ses çal

["Güncellenen hatalar için ses çal" ayarı][4], NVDA 2021.3'te kullanıma sunulmuştur ve bir hata kaydedildiğinde NVDA'nın bir hata sesi çalıp çalmayacağını belirtmeye olanak tanır.

Bu eklenti, bu ayarı değiştirmek için ek bir komut (`NDTTGesture, shift+E`) sağlar.
Şunlardan birini seçebilirsiniz:

* "Yalnızca test sürümlerinde" (varsayılan) seçeneği, NVDA'nın hata seslerini yalnızca mevcut NVDA sürümü bir test sürümü (alfa, beta veya kaynak koddan çalıştırılan) ise çalmasını sağlar.
* Mevcut NVDA sürümünüz ne olursa olsun, hata seslerini etkinleştirmek için "Evet"i seçin.
* "Hayır" seçeneği, mevcut NVDA sürümünüz ne olursa olsun hata seslerini devre dışı bırakmanızı sağlar; bu özellik yalnızca yeni NVDA sürümlerinde mevcuttur.

2021.3 öncesi NVDA sürümleri için bu eklenti, bu özelliğin geriye dönük uyumluluğunu ve klavye komutuyla kontrol edilebilme imkanını sağlar.
Gelişmiş ayarlar panelindeki açılır menü geriye dönük olarak aktarılmamıştır.
NVDA'nın herhangi bir sürümü için hata seslerini devre dışı bırakma özelliği, 2026.2'den önceki sürümler için de geriye dönük olarak uygulanmamıştır.

## Nesne özellik gezgini

Bu özellik, günlük görüntüleyiciyi açmadan mevcut gezinti nesnesinin bazı özelliklerini raporlamaya olanak tanır.

Bir nesnenin özelliklerini listelemek için, gezinti nesnesini o nesnenin üzerine getirin ve aşağıdaki komutları kullanın:

* `NDTTGesture, yukarı ok`: Önceki özelliği seçer ve bunu gezinti nesnesi için rapor eder.
* `NDTTGesture, downArrow`: Sonraki özelliği seçer ve bunu gezinti nesnesi için bildirir.
* `NDTTGesture, N`: Gezinti nesnesi için şu anda seçili olan özelliği bildirir
* `NDTTGesture, shift+N`: Gezinti nesnesi için şu anda seçili olan özelliği, göz atılabilir bir mesajda görüntüler

Desteklenen özelliklerin listesi aşağıdaki gibidir:
ad, rol, durum, değer, windowClassName, windowControlID, windowHandle, konum, Python sınıfı, Python sınıfı mro.

Nesne dolaşım komutlarını kullanırken, NVDA'nın olağan nesne bildirimi yerine, şu anda seçili olan özelliğin bildirilmesini da seçebilirsiniz.
`NDTTGesture, Kontrol+N` komutu, nesnelerin bu özel bildirimi ile NVDA'nın olağan bildirimi arasında geçiş yapmayı sağlar.

Örneğin, "windowClassName" özelliğini seçebilir ve özel nesne bildirimini etkinleştirebilirsiniz.
Ardından, gezinti nesnesini bir sonraki veya önceki nesneye taşıdığınızda, normal raporlama yerine nesnenin windowClassName'ini duyacaksınız.

## Komut dosyası ve kaynak kod araçları

<a id="sourceCodeOpeningCommands"></a>
### Kaynak kodunu açma komutları

Bu eklenti, kaynak kodunu açmaya olanak sağlayan üç komut sunmaktadır.

İlk komut, bir komut dosyasının kaynak kodunu, ilgili hareketini bilerek açmanıza olanak tanır.
Kullanmak için `NDTTGesture, C` tuşlarına basın ve ardından kodunu görmek istediğiniz komut dosyasının hareketini seçin.
Örneğin, ön plandaki pencerenin başlığını bildiren komut dosyasının kodunu görmek için `NDTTGesture, C` tuşlarına ve ardından `NVDA+T` tuşlarına basın.

Diğer iki komut, kaynak kodunu bulunduğu yoldan açmanıza olanak tanır:

* `NDTTGesture, shift+C`, sistem imlecinin altında bulunan yolun kaynak kodunu açar.
* `NDTTGesture, Kontrol+C`, inceleme imlecinin altında bulunan yolun kaynak kodunu açar.

E.g. if the caret or the review cursor is located on the following line, the command will open the corresponding file in your editor:
`C:\Users\username\AppData\Roaming\nvda\addons\addonName\globalPlugins\addonName\__init__.py:48`

Bu komutları kullanabilmek için, eklentinin ayarlarında [favori editörünüzün komutunu](#settingsOpenCommand) yapılandırmış olmanız gerekir.
NVDA'yı kaynak kodundan çalıştırmıyorsanız, [NVDA kaynak kodunun konumu](#settingsNvdaSourcePath) da yapılandırılmış olmalıdır.

### Genişletilmiş komut açıklama modu

Genişletilmiş komut dosyası açıklama modu, girdi yardım kipinde açıklama bulunmayan komut dosyaları hakkında bilgi edinmeyi sağlar.

Genişletilmiş komut dosyası açıklama modu etkin olduğunda, girdi yardımı kipi (NVDA+1) aşağıdaki gibi değiştirilir.
Bir komut dosyasının açıklaması yoksa, komut dosyasının adı ve sınıfı bildirilir.
Bir komutun açıklaması varsa, açıklaması her zamanki gibi bildirilir.
Bu özelliği etkinleştirmek veya devre dışı bırakmak için kullanılan hareket `NDTTGesture, D`'dir.

Girdi yardımı kipinde açıklama içermeyen bir komuta bağlı bir hareketi yürütmek, bu komut için hareket yönetimi iletişim kutusunda bir giriş de oluşturur.
Bu giriş, "Açıklama içermeyen komut dosyaları (değişiklikler kendi sorumluluğunuzdadır!)" adlı özel bir kategoride yer almaktadır.
Bu sayede bu komut dosyaları için yerel NVDA hareketlerini kolayca ekleyebilir, silebilir veya değiştirebilirsiniz.
Ancak, bu tür komut dosyalarının genellikle kullanıcının ilgili hareketi değiştirmesini engellemek amacıyla herhangi bir açıklama içermemesinin amaçlandığını unutmayın.
Gerçekten de, bu hareket bir uygulama kısayol tuşuyla eşleşecek şekilde tanımlanabilir.
Örneğin, NVDAObjects.window.winword.WordDocument üzerindeki script_toggleItalic komut dosyası Ctrl+I tuş kombinasyonuna bağlıdır ve bu değiştirilmemelidir çünkü kısayol tuşunun gerçekten çalıştırılması için hareket uygulamaya iletilir.

#### Kullanım örneği

Ctrl+Shift+I tuşlarına basmak, NVDA tarafından doğal olarak desteklenmese bile Word'de italik yazı tipini açıp kapatmayı sağlar.
NVDA'nın Control+I sonucunu Control+I olarak bildirmesi için aşağıdaki adımları uygulamanız gerekir:

* Bir Word belgesi açın.
* `NDTTGesture, D` komutuyla genişletilmiş komut açıklama modunu etkinleştirin.
* NVDA+1 tuş kombinasyonuyla girdi yardım kipine girin.
* İtalik metni bildirmek ve hareket iletişim kutusuna eklemek için Ctrl+I tuşlarına basın.
* NVDA+1 tuş kombinasyonuyla girdi yardım modundan çıkın.
* Girdi hareketleri iletişim kutusunu açın.
* "Açıklama içermeyen komut dosyaları (kendi sorumluluğunuzda değiştirin!)" kategorisinde, "NVDAObjects.window.winword.WordDocument üzerinde toggleItalic" komutunu seçin.
* Ctrl+Shift+I kısayolunu ekleyin ve onaylayın.
* İsterseniz, `NDTTGesture, D` komutuyla genişletilmiş komut dosyası açıklama modundan çıkabilirsiniz.

Bilinen hata: Belirli bir sınıf için eklenen bir komut dosyası, hareket yöneticisi başka bir bağlamda açılmış olsa bile görünür durumda kalıyor.

## Günlük okuma ve analiz özellikleri

<a id="logPlaceMarkers"></a>
### Günlüğe işaretler yerleştirin

Test yaparken veya çalışırken, daha sonra günlüğü okurken kolayca geri dönebilmek için günlüğe belirli bir anı işaretlemek isteyebilirsiniz.
Günlüğe işaretleyici mesaj eklemek için `NDTTGesture, K` tuşlarına basın.
A message as follows will be logged at INFO level:
`-- NDTT marker 0 --`

Günlüğe istediğiniz kadar işaretleyici ekleyebilirsiniz.
Günlüğe her işaretleyici yerleştirdiğinizde işaretleyicinin numarası artırılacaktır; yalnızca NVDA yeniden başlatıldığında sıfırlanacaktır.

### Günlük okuyucu modu

Günlük okuma modu, günlüklerin okunmasını ve analizini kolaylaştırmak için komutlar sağlar.
Günlük görüntüleyici penceresinde ve Python konsol çıktı alanında, günlük okuyucu varsayılan olarak etkinleştirilmiştir, bu nedenle günlük okuma komutları hemen kullanılabilir.
Bir düzenleyici (örneğin Notepad++) veya bir web sayfası (örneğin GitHub sorunu) gibi başka bir metin okuma alanında, günlük okuyucu modunu etkinleştirmek ve komutlarını kullanmak için `NDTTGesture, L` tuşlarına basmanız gerekir.
Günlük okuma ve analiz işlemleriniz bittiğinde, günlük okuyucu modunu devre dışı bırakmak için `NDTTGesture, L` komutunu tekrar devre dışı bırakabilirsiniz.

Aşağıda, günlük okuyucu modunda kullanılabilen komutlar açıklanmıştır.
Bu modda, mevcut tüm komutları görüntülemek için `control+H` tuşlarına da basabilirsiniz.

<a id="logReaderQuickNavigationCommands"></a>
#### Hızlı dolaşım komutları

Tek harfli komutlar, tarama modundaki hızlı dolaşım tuşlarına benzer şekilde, çeşitli türdeki günlük mesajlarına geçmeyi sağlar:

* m: herhangi bir mesaj
* e: hata mesajları (`ERROR` ve `CRITICAL`)
* w: uyarı mesajları (`UYARI`)
* f: bilgi mesajları (`INFO`)
* k: daha önce [günlüğe yerleştirilen](#logPlaceMarkers) işaretleyiciler
* g: hata ayıklama uyarı mesajları (`DEBUGWARNING`)
* i: Girdi/çıktı mesajları (`IO`)
* n: girdi mesajları
* s: konuşma mesajları
* b: braille mesajlar
* d: hata ayıklama mesajları (`DEBUG`)

Tek harfe basmak, bu mesajın bir sonraki gösterimine geçmenizi sağlar.
Harfi Shift tuşuyla birlikte kullanmak, bu mesajın önceki gösterimine geçmenizi sağlar.

Ayrıca, belirli mesaj türlerinde, `O` veya `shift+O` tuşlarına basarak blok blok atlayabilirsiniz.
Aşağıdaki mesaj türleri ve bunlarla ilişkili bloklar desteklenmektedir:

* Hata mesajları gibi izleme bilgileri içeren mesajlarda, blok dolaşımı izleme bilgileri arasında geçiş yapmanıza olanak tanır
  Bu, özellikle birden fazla hata izleme çıktısı olduğunda, örneğin bir try/except bloğunun "except" kısmında bir hata oluştuğunda kullanışlıdır.
* Bir donma meydana geldiğinde kaydedilen Python iş parçacıklarının yığınlarını listeleyen mesajda, blok dolaşımı iş parçacığı yığınları arasında geçiş yapmanıza olanak tanır.
* `NVDA+F1` tuşuna bastığınızda kaydedilen, gezinti nesnesine ilişkin geliştirici bilgilerini içeren mesajda, blok dolaşımı özellik grupları arasında geçiş yapmanıza olanak tanır.
  Özelliklerin dört grubu vardır: genel özellikler, uygulama modülü özellikleri, pencere özellikleri ve arayüze özgü (IAccessible, UIA) özellikler.

Son olarak, bir blok içinde, bloğun ilginizi çeken ilk veya son satırına hızlıca geçmek isteyebilirsiniz.
Geçerli bloğun içeriğinin ilgilendiğiniz ilk satırına, örneğin bir hata izleme kaydının ilk karesine atlamak için `shift+L` tuş kombinasyonunu kullanın.
Blok içeriğinin son satırına atlamak için `L` tuşunu kullanın; örneğin, bir iş parçacığı yığınının son karesi veya bir hata izleme kaydının altındaki hata.

#### Konuşma mesajının çevirisi

Bazen, anlamadığınız yabancı bir dilde yazılmış bir sistemde tutulan bir kaydı incelemeniz gerekebilir.
Örneğin, kayıt Çin sistemi/NVDA üzerinden alınmış, oysa siz sadece Fransızca biliyorsunuz.
[Anında Çeviri][3] eklentisini yüklediyseniz, konuşma mesajlarının çevrilmesi için [hızlı günlük Dolaşım komutlarıyla](#logReaderQuickNavigationCommands) birlikte kullanabilirsiniz.

* Öncelikle Anında Çeviri'nin dillerini yapılandırın.
  Kaynak dil, günlük kaydının alındığı sistemin dili olmalıdır (örneğin Çince).
  Hedef dil, sizin ana diliniz olmalıdır (örneğin Fransızca).
* Günlüğü açın
* Günlük dosyasında otomatik konuşma çevirisini etkinleştirmek için `Ctrl+T` tuşlarına basın
* Günlük dosyasında Hızlı dolaşım komutlarını kullanın, örneğin S, I, vb. Bir sesli mesajla karşılaşıldığında, bu mesaj sizin dilinizde (önceki örneğimizde Fransızca) seslendirilecektir.

Sesli çeviriyi devre dışı bırakmak istiyorsanız, tekrar `control+T` tuşlarına basın.

<a id="logReaderOpenSourceFile"></a>
#### Kaynak kod dosyasını editörünüzde açın

Günlük dosyasında bazı satırlar kaynak koduna atıfta bulunabilir:

* A line belonging to a traceback contains the path and the line in a file, e.g.:
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`
* The header line of a logged message contains the function which has logged this message, e.g.:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`
* The content of a message logged in input help mode (logged at info level):
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`

Hata izleme kaydının veya kaydedilen mesajın içeriğini anlamak için bu kodu içeren dosyayı açmak isteyebilirsiniz.
Bu dosyayı açmak için C tuşuna basmanız yeterli.

Bu özelliği kullanabilmek için, eklentinin ayarlarında [favori editörünüzün komutunu](#settingsOpenCommand) yapılandırmış olmanız gerekir.
NVDA'yı kaynak kodundan çalıştırmıyorsanız, [NVDA kaynak kodunun konumu](#settingsNvdaSourcePath) da yapılandırılmış olmalıdır.

#### Geri izleme analizi

Sometimes you may have error tracebacks in the log, as in the following example:

    HATA - scriptHandler.executeScript (14:47:43.426) - MainThread (15492):
komut dosyasını yürütürken hata oluştu: <bound method LogContainer.script_openSourceFile of <NVDAObjects.Dynamic_LogViewerLogContainerIAccessibleRichEdit50WindowNVDAObject object at 0x34C1E510>> with gesture 'c'
    İzleme kaydı (en son çağrı):
      "scriptHandler.pyc" dosyasında, 300. satırda, executeScript fonksiyonunda
      "C:\Users\myUserName\AppData\Roaming\\nvda\\addons\\nvdaDevTestToolbox\globalPlugins\\ndtt\logReader.py" dosyasında, 603. satırda, script_openSourceFile fonksiyonunda
        if self.openStackTraceLine(satır):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      Dosya "C:\Users\myUserName\AppData\Roaming\\nvda\\addons\\nvdaDevTestToolbox\globalPlugins\\ndtt\logReader.py", satır 667, openStackTraceLine içinde
        0 / 0 # Hatalı bir kod satırı
        ~~^~~
    ZeroDivisionError: sıfıra bölme

Kaynak kodunun mevcut olduğu karelerde, `^` (şapka) ve `~` (tilde) karakterleriyle işaretlenmiş görseller fark etmiş olabilirsiniz.
Python, hata izleme çerçevesinde hatanın konumunu ve bağlamını görsel olarak bu şekilde gösterir.
`Ctrl+E` tuşlarına basmak, imleci kaynak kod satırındaki hatanın başına, yani `^` (şapka) karakteriyle işaretlenmiş metne taşır.
Bu metni seçmek için çift tıklayın.
Üç basış, hatayı bağlamıyla birlikte, yani `^` (şapka) ve `~` (tilde) karakterleriyle işaretlenmiş kaynak kod satırının metniyle birlikte seçer.

Lütfen dikkat: 2024.1 öncesi bir NVDA sürümüyle (yani Python 3.7 veya daha eski bir sürümle) alınan günlüklerde, Python hatayı yalnızca tek bir `^` (şapka) karakteriyle gösterir.
Dolayısıyla bu komutun çift veya üç basış eylemleri oldukça işlevsiz hale gelir.

#### Mevcut komutların özetini alma

Günlük okuma modunda kullanılabilen tüm komutların listesini görüntülemek için `control+H` tuşlarına basın.

## Bir günlüğü anonimleştirin

Sorunları bildirirken, bir kayıt dosyası sağlamanız gerekebilir.
Ancak, kayıtlar hassas bilgiler (kullanıcı adları, e-postalar vb.) içerebilir.
Bu eklenti, bir günlük dosyasının içeriğini anonimleştirmek için bir komut sağlar.

Günlük kaydının bir bölümünü veya tamamını seçin ve `NDTTGesture, A` tuşlarına basın.
Anonimleştirilmiş günlük içeriği panoya kopyalanacaktır.
Mevcut seçimin üzerine yapıştırarak değiştirebilir veya dilediğiniz başka bir yere yapıştırabilirsiniz.

Bu özelliği kullanmak için, bu komut tarafından kullanılan anonimleştirme kurallarını özelleştirmeniz gerekir.
Bu kuralları yapılandırmak için kullanılan dosya şu konumda bulunur: `pathToNVDAConfig\\ndtt\\anonymizationRules.dic` (örneğin, `C:\Users\myUserName\AppData\Roaming\\nvda\\ndtt\\anonymizationRules.dic`).
Bu dosyayı yazmak için gereken tüm talimatları dosyanın başlık kısmında bulabilirsiniz.
Anonimleştirme kuralları dosyanızı bozduysanız veya başlık talimatlarını sildiyseniz, bu dosyayı silin veya yeniden adlandırın; bir sonraki başlatmada bu dosyanın yeni bir sürümü oluşturulacaktır.

<a id="oldLogsBackup"></a>
## Eski kayıtların yedeklenmesi

NVDA, önceki NVDA oturumunun günlük dosyasının yedeğini zaten sağlıyor; dosyanın adı `nvda-old.log`.
Ancak bazen daha eski günlük dosyalarına erişmek isteyebilirsiniz; örneğin, `nvda-old.log` dosyasına bakmadan önce NVDA'yı yeniden başlatmanız gerekmiş olabilir.
Bu eklenti, eski günlüklerin yedeklenip yedeklenmeyeceğini ve kaç tanesinin yedekleneceğini yapılandırmanıza olanak tanır; bu işlem [eklentinin ayarlarında](#settingsLogsBackup) yapılır.

Bir günlük yöneticisi iletişim kutusu, yedeklenen günlükleri görüntülemenizi sağlar.
NVDA menüsüne gidip Araçlar -> Günlük yöneticisi yolunu izleyerek açabilirsiniz
Bu iletişim kutusunda, tüm yedekleme günlüklerinin listesini görebilir ve seçilen günlük üzerinde çeşitli işlemler gerçekleştirebilirsiniz:

* (Enter tuşuna basarak) açın
* sil (`Delete` tuşuna basın)
* günlük dosyasını kopyala (`Ctrl+C` tuşlarına basın).

Birden fazla kayıt seçerek hepsine ayrı ayrı işlem uygulayabilirsiniz.

Bir günlük dosyasını açabilmek için öncelikle [Dosyayı favori düzenleyicinizde açmak için kullanılan komutu](#settingsOpenCommand) yapılandırmış olmanız gerekir.

## Python konsol uzantısı

<a id="pythonConsoleOpenCodeFile"></a>
### `openCodeFile` fonksiyonu

In the console, you can call the following function to view the source code that defines the variable `myVar`:
`openCodeFile(myVar)`

Bu özelliğin çalışması için, eklentinin ayarlarında [favori editörünüzün komutunu](#settingsOpenCommand) yapılandırmış olmanız gerekir.
NVDA'yı kaynak kodundan çalıştırmıyorsanız, [NVDA kaynak kodunun konumu](#settingsNvdaSourcePath) da yapılandırılmış olmalıdır.

`openCodeFile` fonksiyonları, NVDA'nın kodunda tanımlanan nesneler veya eklentiler tarafından tanımlanan nesneler üzerinde çağrılabilir.
Kaynak koduna erişilemeyen nesneler üzerinde (örneğin Python'ın yerleşik fonksiyonları) bu fonksiyon çağrılamaz.

Nesneyi henüz konsola aktarmadıysanız, adını `openCodeFile` fonksiyonuna parametre olarak da iletebilirsiniz.

Aşağıda NVDA kodundaki çağrı örnekleri verilmiştir:

* View the definition of the function `speech.speech.speak`:
  `openCodeFile(speech.speech.speak)`
  or with the name passed as parameter:
  `openCodeFile("speech.speech.speak")`
* View the definition of the class `TextInfo`:
  `openCodeFile(textInfos.TextInfo)`
* View the definition of the method `copyToClipboard` of the class `TextInfo`:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`
* View the definition of the class of the focused object:
  `openCodeFile(focus)`
* Open the file `api.py` defining the module `api`:
  `openCodeFile(api)`

### Python konsol başlatma komutu

Python konsolu ilk açıldığında konsol ad alanında çalıştırılacak özel bir komut dosyası tanımlayabilirsiniz.

For example, the script allows you to execute new imports and define aliases that you will be able to use directly in the console, as shown below:

    # Konsolda görmek istediğim çeşitli içe aktarma işlemleri.
    import globalVars as gv
    import core
    import ui
    # Takma Adlar
    ocf = openCodeFile

The Python console script should be placed in the following location: `pathToNVDAConfig\ndtt\consoleStartup.py`
Örneğin: `C:\Users\myUserName\AppData\Roaming\\nvda\\ndtt\consoleStartup.py`

Not: Python 2'de, yani NVDA 2019.2.1 veya daha önceki sürümlerde, yalnızca saf ASCII yazı tipleri desteklenir; Unicode gibi diğer kodlamalar desteklenmez.

### Python konsol girdi geçmişini koruma

Python konsol geçmişinde, önceki girdileri incelemek ve değiştirmek için yukarı ve aşağı ok tuşlarını kullanabilirsiniz.
Ancak, NVDA'dan çıkıldığında önceki girdilerin listesi temizlenir.
Bu eklenti, varsayılan olarak etkinleştirilmiş olan [bir seçenek](#settingsPreserveHistory) sunarak NVDA yeniden başlatıldığında bile Python konsol giriş geçmişinin korunmasını sağlar.

<a id="loggingFunctionCall"></a>
## Fonksiyon çağrılarını kaydetme

Bazen, kodun hangi bölümünün bir şeyi söylemekten sorumlu olduğunu görmek isteyebilirsiniz.
Bunun için, `NDTTGesture, S` tuşlarına basarak `speech.speech.speak` fonksiyonu için fonksiyon çağrılarının günlüğe kaydedilmesini etkinleştirebilirsiniz.
NVDA her konuştuğunda, yığın izi de dahil olmak üzere ilgili bir mesaj kaydedilir; bu da konuşma çıktısına neden olan kodu belirlemenizi sağlar.
İşiniz bittiğinde, aynı hareketi kullanarak fonksiyon çağrılarının kaydedilmesini devre dışı bırakın.

Aynı şekilde, bir bip sesinin, Braille çıktısının veya bir sesin (örneğin yazım hatası sesi) kaynağını izlemek için `tones.beep`, `braille.BrailleBuffer.update` veya `nvwave.playWaveFile` çıktı fonksiyonlarının çağrılarını kaydetmeyi seçebilirsiniz.
[Hedef fonksiyon](#targetFunctionForCallLogSetting), eklentinin parametrelerinden seçilebilir.
Hatta özel bir fonksiyonun çağrı yığınını bile kaydedebilirsiniz.

Varsayılan olarak, fonksiyon çağrılarının kaydı "settrace" yöntemi kullanılarak yapılır: hedef fonksiyonun dönüş olayında çağrılan bir izleme geri çağırma işlevi kurmak için `sys.settrace`, `threading.settrace` ve/veya `threading.settrace_all_threads` kullanılır.
Alternatif olarak, tatmin edici sonuçlar alamazsanız, hedef fonksiyonun (örneğin `speech.speech.speak`) yamalandığı "maymun yaması" yöntemini tercih edebilirsiniz.
Her iki yöntemin de, belirli kombinasyon koşullarında fonksiyon çağrılarının kaydedilmesini engelleyebilecek sınırlamaları vardır.
Örneğin, hedef fonksiyon ana iş parçacığı dışında bir iş parçacığından çalıştırıldığında ve hedef fonksiyonun iş parçacığı başlatıldıktan sonra fonksiyon çağrılarının günlük kaydı etkinleştirildiğinde, "settrace" yöntemi 2026.1'den düşük NVDA sürümlerinde çalışmayabilir.
Öte yandan, hedef fonksiyon "from import" ifadesiyle (örneğin `from tones import beep`) içe aktarıldığında "monkey patching" yöntemi çalışmayabilir.

Fonksiyon çağrılarını kaydetmek için kullanılan yöntemi [özel ayar](#functionCallLogMethodSetting) üzerinden veya `NDTTGesture, shift+S` tuşlarına basarak değiştirebilirsiniz.

<a id="reverseTranslationCommand"></a>
## Ters çeviri komutu

Birçok test uzmanı NVDA'yı İngilizce dışında başka bir dilde kullanmaktadır.
Ancak GitHub'da test sonuçlarını bildirirken, değiştirilen seçeneklerin açıklaması veya NVDA tarafından bildirilen mesajlar İngilizce olarak yazılmalıdır.
Seçeneklerin veya mesajların tam metnini kontrol etmek için NVDA'yı İngilizce olarak yeniden başlatmak oldukça sinir bozucu ve zaman alıcı.

Bunu önlemek için, eklenti, NVDA'nın arayüzündeki mesajlar, GUI'deki kontrol etiketleri vb. öğeleri tersine çevirmeye olanak tanıyan iki ters çeviri komutu sağlar.

* `NDTTGesture, R`, son konuşmayı tersine çevirmek için NVDA'nın gettext çeviri fonksiyonunu kullanır.
* `NDTTGesture, shift+R` komutu, son konuşmanın tersine çevirisini yapmak için NVDA ve eklentilerinden gettext çevirilerini kullanır.

Daha spesifik olarak, son konuşma dizisinin ilk dizesi tersine çevrilir.

Örneğin, Fransızca NVDA'da, "Outils" adlı Araçlar menüsüne aşağı ok tuşuyla gidersem, NVDA "Outils sous-Menu o" diyecek, bu da "Araçlar alt menüsü o" anlamına gelir.
Eğer hemen ardından ters çeviri komutunu basarsam, NVDA "Outils" kelimesini "Tools" olarak ters çevirecektir.

Daha sonra kayıtlara baktığımızda şu satırları buluyoruz:

    IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
    Speaking ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (still valid)]

Bu, "Outils"in konuşma dizisindeki ilk dize olduğunu doğrular.

Ters çeviri iki veya daha fazla olası sonuca yol açarsa, tüm olasılıkları listeleyen bir bağlam menüsü açılır.

Ters çevirinin sonucu, ilgili [seçenek](#settingsCopyReverseTranslation) etkinleştirilmişse (varsayılan değer) panoya da kopyalanır.

NVDA dizelerinin ters çevirisi yalnızca NVDA 2022.1 veya üzeri sürümlerde mevcuttur.
NVDA'nın önceki sürümlerinde, ters çeviri için yalnızca eklenti dizeleri kullanılabilir.

Ayrıca, NVDA'nın 2019.2.1 veya daha önceki sürümlerinde, ters çeviri bulunamadığı takdirde, dizenin ilk bölümünde ikinci bir deneme yapılır.
Gerçekten de, bu NVDA sürümlerinde konuşma dizisi şu şekilde görünmektedir:

    IO - speech.speak (12:39:12.684):
    Speaking [u'Outils  sous-Menu  o']

Nesne etiketinin rol, durum, kısayol vb. ile birleştirilebileceğini görebiliriz.
Dolayısıyla, ters çeviri tüm dizeyle sonuç vermezse, çift boşluktan (" ") önceki dize bölümü üzerinde ikinci bir deneme yapılır.
Ancak bu da kusursuz bir yöntem değil, çünkü bir dizenin aslında çift boşluk içerme olasılığını göz ardı edemeyiz.

<a id="settings"></a>
## Ayarlar

Eklentinin bazı özellikleri belirli bir yapılandırma gerektirebilir.
Ayarlar paneli, bu özellikleri etkinleştirmenize veya nasıl çalıştıklarını kontrol etmenize olanak tanır.
Bu ayarları görüntülemek ve değiştirmek için NVDA menüsüne gidin -> Tercihler'i seçin ve NVDA Geliştirici ve Test Araç Kutusu kategorisini seçin.
Bu ayarlar iletişim kutusuna, Günlük Yöneticisi iletişim kutusundan da doğrudan erişilebilir.

Bu ayarlar geneldir ve yalnızca varsayılan profil etkin olduğunda yapılandırılabilir.

<a id="settingsOpenCommand"></a>
### Dosyayı favori editörünüzde açmak için komut

Bazı özellikler, içeriği favori editörünüzde görüntülemenize olanak tanır.
Bu, kaynak dosyayı [bir günlükten](#logReaderOpenSourceFile), [konsoldaki bir nesneden](#pythonConsoleOpenCodeFile) veya [yazılı bir hareketten](#sourceCodeOpeningCommands) görüntüleme komutlarının yanı sıra [günlük yöneticisinin](#oldLogsBackup) Aç düğmesini de içerir.

Bunları kullanabilmek için öncelikle dosyayı favori editörünüzde açmak üzere çağrılacak komutu yapılandırmanız gerekir.
The command should be of the form:
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`
Elbette bu satırı, kullandığınız düzenleyicinin gerçek adına ve konumuna ve dosyaları açmak için kullandığı söz dizimine göre değiştirmeniz gerekir.
`{path}`, açılacak dosyanın tam yoluyla, `{line}` ise imlecin yerleştirilmesini istediğiniz satır numarasıyla değiştirilecektir.
For Notepad++ for example the command to type in the console would be:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### NVDA kaynak kod yolu

[Günlük dosyasından](#logReaderOpenSourceFile), [konsoldaki bir nesneden](#pythonConsoleOpenCodeFile) veya [yazılan bir hareketten veya bir yoldan](#sourceCodeOpeningCommands) kaynak dosyayı görüntülemek için bir komut kullanıldığında, dosya NVDA'nın kendisine ait olabilir.
Eğer NVDA'yı kaynak koddan çalıştırmıyorsanız, NVDA'nız yalnızca derlenmiş dosyaları içerir.
Bu sayede, ilgili kaynak dosyasının bulunacağı alternatif bir konumu burada belirtebilirsiniz; örneğin, NVDA kaynak dosyalarını kopyaladığınız yer gibi, böylece kaynak dosya her halükarda açılabilir.
The path should be such as:
`C:\pathExample\GIT\nvda\source`
Elbette, NVDA kaynak dosyasının yolunu doğru olanla değiştirin.

Ancak kaynak dosyanızın sürümünün (örneğin GIT commit'i) NVDA'nın çalışan örneğinin sürümüyle aynı olduğundan emin olun.

<a id="settingsLogsBackup"></a>
### Eski kayıtların yedeklenmesi

Eski günlüklerin yedeklenmesi açılır menüsü, [özelliği](#oldLogsBackup) etkinleştirmenize veya devre dışı bırakmanıza olanak tanır.
Etkinleştirilirse, aşağıda "Yedekleme sayısını sınırla" bölümünde saklamak istediğiniz maksimum yedekleme sayısını da belirtebilirsiniz.
Bu ayarlar yalnızca yedekleme işleminin gerçekleştiği bir sonraki NVDA başlatılışında geçerli olur.

<a id="settingsCopyReverseTranslation"></a>
### Ters çeviriyi panoya kopyala

Bu seçenek, [ters çeviri komutunun](#reverseTranslationCommand) sonucunu panoya kopyalayıp kopyalamayacağını seçmenize olanak tanır.

<a id="settingsPreserveHistory"></a>
### Yeniden başlatmanın ardından konsol giriş geçmişini koru

Bu onay kutusu işaretlenirse, NVDA yeniden başlatıldığında Python konsol giriş geçmişi korunacaktır.
Bu seçenek işaretlenirse, kaydedilecek maksimum giriş sayısını da aşağıda belirtebilirsiniz.
Bu seçenek işaretlenmezse, NVDA normal şekilde çalışır, yani yeniden başlatmanın ardından konsol geçmişi boş kalır.

<a id="targetFunctionForCallLogSetting"></a>
### Fonksiyon çağrısı kaydı için hedef fonksiyon

Bu açılır liste, [işlev çağrısı günlüğünü](#loggingFunctionCall) etkinleştirildiğinde çağrıları günlüğe kaydedilecek işlevi tanımlar.
Çeşitli çıktı fonksiyonları arasından seçim yapabilir veya özel fonksiyon seçeneğini tercih edebilirsiniz.

Özel fonksiyon seçeneğini seçerseniz, çağrılarını kaydetmek istediğiniz fonksiyonun tam adını girmeniz gerekecektir.
Bu tam ad, konumunu (paket, modül, sınıf vb.) içermelidir.
Fonksiyonu, tanımlandığı asıl konumla birlikte tanımlamaya dikkat edin, aksi takdirde çağrı kaydı tutma işlemi daha az başarılı olacaktır.
Örneğin, `speech\__init__.py` dosyasında içe aktarılan sembolü hedefleyen `speech.getCurrentLanguage` yerine, `speech\speech.py` dosyasında tanımlanan işlevi hedefleyen `speech.speech.getCurrentLanguage` kullanın.

<a id="functionCallLogMethodSetting"></a>
### Fonksiyon çağrı günlüğü yöntemi

Bu açılır liste, [işlev çağrısı kaydı](#loggingFunctionCall) etkinleştirildiğinde işlev çağrılarını tanımlamak için kullanılan yöntemi belirler.
Bu parametre, `NDTTGesture, shift+S` tuşlarına basılarak da değiştirilebilir.
Bu yöntem değiştirildiğinde, değişiklik öncelikle fonksiyon çağrı günlüğü bir sonraki etkinleştirildiğinde uygulanır; yani, şu anda etkin olan fonksiyon çağrı günlüğüne uygulanmaz.

## Değişiklik günlüğü

### Sürüm 10.1

* Komut giriş noktası hareketi, yeni "son konuşmayı tekrarla" komutuyla çakışmayı önlemek için `NVDA+Z` olarak değiştirildi.
* "Kayıt altına alınan hatalar için ses çal" komutu, NVDA 2026.2'de tanıtılan "Hayır" değerini destekleyecek şekilde güncellendi.

### Sürüm 10.0

* Günlük okuyucu: Fonksiyon çağrıları kaydedilirken, argümanlar ve dönüş değerleri de artık kaydediliyor. (hwf1324'ün katkısıyla)
* Günlük okuyucu: Gezinme komutları kullanılırken, bazı mesajlar artık kısaltılmış veya boş olarak raporlanmıyor.
* Son hata bildirilirken, bazı mesajlar artık enterpolasyon yapılmadan bildirilmiyor (örneğin, "%s" içeren mesajlar).
* NVDA 2019.2'deki bazı hatalar düzeltildi: Python konsol geçmişinin ilk kullanımı, Nesne özellik gezgini ile ASCII olmayan nesne adlarının raporlanması.
* NVDA 2026.1 ile uyumludur.

### Sürüm 9.0

* İmleç dosya yolunda/satırında olduğunda kod dosyasını açan yeni bir komut eklendi.
* Fonksiyon çağrılarının kaydedilmesi (önceden yığın kaydı olarak biliniyordu) geliştirildi ve herhangi bir fonksiyonun çağrısını kaydetme olanağı sunularak fonksiyon çağrılarını tanımlamak için daha güvenilir bir yöntem sağlandı.
* Günlük okuyucu ile ilgili bir güvenlik sorunu düzeltildi ([GHSA-39pg-6xpm-mjgf](https://github.com/CyrilleB79/NVDA-Dev-Test-Toolbox/security/advisories/GHSA-39pg-6xpm-mjgf)).
* NVDA 2019.2.1 ile artık IO bip sesleri doğru şekilde raporlanıyor.
* Günlük okuma komutları artık bazı konuşma komutlarını (örneğin Console Toolkit eklentisi kullanılırken) okuyamama sorunu yaşamıyor.
* Birden fazla olası ters çeviri durumunda, hangi öğeye tıklandığına bakılmaksızın son menü öğesinin panoya kopyalanması sorunu giderildi.
* NVDA 2026.1 ile uyumluluk hazırlandı

### Sürüm 8.0

* Python konsol geçmişi artık yeniden başlatmalar arasında korunabiliyor.
* Ters çeviri: Hem NVDA hem de eklentilerinin çevirilerini kullanarak bir dizeyi ters çevirmek için ikinci bir komut eklendi.
* Yeni günlük okuyucu komutları, önceki veya sonraki Braille çıktı mesajına atlamayı sağlar
* Yeni günlük okuyucu komutu, bir mesajdaki önceki veya sonraki bloğa atlamayı sağlar; örneğin, bir izleme raporundaki önceki veya sonraki iş parçacığı yığınına, gezgin nesnesi için geliştirici bilgilerindeki önceki veya sonraki özellik bloğuna vb.
* Yeni log okuyucu komutları, bir bloğun ilk veya son ilgi çekici satırına atlamayı sağlar; örneğin, bir hata izleme kaydının ilk veya son karesine
* Yeni bir günlük okuyucu "Hataya git" komutu, izleme çerçevesindeki hataya atlamayı sağlar.
* Günlük dosyasını okurken mevcut tüm komutları listeleyen bir yardım mesajı görüntüleyen yeni bir günlük okuyucu komutu.
* Python konsol çıktı bölmesinde günlük okuma modu artık varsayılan olarak etkinleştirilmiştir.
* Günlük dosyasını anonimleştirmek için yeni bir komut
* Konsol başlatma komutu artık Unicode dizelerini destekliyor (yalnızca Python 3 için); ancak tam Unicode dosyaları desteklenmeyebilir.
* Python konsolu başlatma komutu artık yalnızca konsol açıldığında bir kez çalıştırılacaktır.
Eklentiler yeniden yüklendiğinde bu komut dosyasının birçok kez çalıştırılabilmesine neden olan bir hata düzeltildi.
* Konsol başlatma komutunda hata yönetimi iyileştirildi.
* Hata düzeltmesi: Günlük kaydı devre dışı bırakıldığında oluşturulan boş günlük dosyaları artık eski günlük olarak kaydedilmiyor.
* Katman komutlarında artık isteğe bağlı konuşma özelliği desteklenmektedir
* Komut dosyasını açan komutun hata işleme özelliği iyileştirildi (yanlış veya eksik yapılandırma durumunda veya Braille ekranı kullanıldığında).

### Sürüm 7.3

* Hata düzeltmesi: Eklentinin katman komutlarını etkinleştirme komutuna artık başka bir hareket de atanabilir.

### Sürüm 7.1

* NVDA 2025.1 ile uyumludur.

### Sürüm 7.0

* Layered commands have been introduced; the entry point is `NVDA+X`.
  The existing commands have been modified accordingly.
* Son konuşulan mesajı tersine çevirmek için yeni bir komut (`NVDA+X, R`).
* Sonraki basılan harekete karşılık gelen komut dosyasının kaynak kodunu açmak için yeni bir komut (`NVDA+X, C`) eklendi.
* İsteğe bağlı konuşma desteği eklendi.
* Günlük yöneticisi artık, diyaloglardaki özel düğmelerle veya listedeki klavye kısayollarını kullanarak daha fazla işlem yapılmasına olanak tanıyor: günlüğü açmak için `enter`, günlük dosyasını kopyalamak için `control+C` ve günlük dosyasını silmek için `delete`.
* Günlük yöneticisindeki sıralama düzeni tersine çevrildi (en yeni günlük en üstte).
* OpenCodeFile fonksiyonu ile Python modülü açmaya çalışırken oluşan bir sorun düzeltildi.

### Version 6.3

* NVDA 2024.1 ile uyumludur.

### Sürüm 6.2

* NVDA < 2021.1 sürümleri için konsol açma özelliğini geri yükler.
* NVDA'nın eski sürümleriyle eklentiyi kullanırken [GHSA-xg6w-23rw-39r8][5] ile ilgili olası güvenlik sorunları ele alındı.
Ancak NVDA 2023.3.3 veya daha üst sürümünün kullanılması önerilir.

### Sürüm 6.1

* Bir paketin alt modülünde bulunan bir nesnenin kaynak dosyasını açma işlemi artık çalışıyor.
* Hata düzeltmesi: Geliştirilmiş çıkış iletişim kutusu, kapatıldıktan sonra beklendiği gibi yeniden açılabilir ve kullanılabilir. (Łukasz Golonka'nın katkısı)

### Sürüm 6.0

* Nesne dolaşım komutları kullanılırken, NVDA'nın olağan nesne bildirimi yerine belirli bir nesne özelliği bildirilebilir.
* Günlük okuma modunda, günlükten bir kod dosyasını açmak için kullanılan "C" tuşu artık girdi yardımı mesajında ​​da çalışıyor.
* Hata düzeltmesi: Kaydedilecek günlük sayısı maksimum değere ayarlandığında eklenti artık başarıyla başlatılabiliyor.
* Hata düzeltmesi: Python konsol başlatma betiğinin çıktısı, sonuç gezinme komutları kullanılırken konsoldaki ilk sonuca atlamayı artık engellemiyor.
* Not: Bundan böyle, yerelleştirme güncellemeleri değişiklik günlüğünde görünmeyecektir.

### Sürüm 5.0

* Anında Çeviri eklentisi yüklüyse, artık günlük okuma komutlarını kullanırken konuşma mesajlarının anında çevrilmesi mümkün.
* Günlük okuma modundayken, E veya Shift+E tuşuna basmak artık normal HATA mesajlarının yanı sıra KRİTİK hata mesajlarına da atlama sağlıyor.
* Girdi ve konuşma mesajlarına hızlıca geçmek için yeni günlük hızlı gezinme komutları eklendi.
* A new command allow to place a marker in the log; and specific quick navigation commands in log reading mode allow to jump to them.
  Credit: the initial idea for this feature comes from Debug Helper add-on by Luke Davis.
* Hata düzeltmesi: Son hatanın hafızaya alınması artık bazı durumlarda başarısız olmuyor.
* Hata düzeltmesi: Eklenti, NVDA 2019.2.1 ile tekrar başlatılabiliyor.
* Hata düzeltmesi: Günlük kaydetme özelliği artık ASCII olmayan günlük dosyalarıyla başarısız olmayacak.

### Sürüm 4.2

* 2021.3'ün altındaki NVDA sürümlerinde oluşan bir hata düzeltildi.
* Hata izleme günlüğü biçimlendirmesi düzeltildi.
* İlk yerelleştirmeler.

### Sürüm 4.1

* Hata kaydı oluşturulurken bazı durumlarda ortaya çıkan bir hata düzeltildi.
* Artık eklentinin ayarları yalnızca varsayılan profil etkin olduğunda değiştirilebiliyor, böylece yapılandırma sorunları önleniyor.

### Sürüm 4.0

* Eski kayıtların yedeklenmesi ve kayıt yöneticisinin kullanıma sunulması imkanı.
* Son kaydedilen hatanın bildirilmesi için bir komut eklendi.
* Eski NVDA sürümlerinde son günlük mesajının okunmasını engelleyen bir hata düzeltildi.

### Sürüm 3.2

* NVDA 2023.1 ile uyumludur.

### Sürüm 3.1

* Bir nesneye ait mevcut olmayan bilgileri isterken oluşan bir hata düzeltildi.

### Sürüm 3.0

* Artık bir log dosyasında, mesajın başlık satırına C tuşuna basarak o mesajı oluşturan fonksiyonu/modülü açabilirsiniz.
* Konsolda, `openCodeFile` fonksiyonu artık parametre olarak nesneyi veya adını içeren bir dizeyi alabilir.
* Yeni özellik: NVDA konsolunu başlatma dosyası: Eğer mevcutsa, YourNVDAConfigFolder\\ndtt\consoleStartup.py dosyası NVDA konsolu ilk açıldığında veya eklentiler yeniden yüklendiğinde çalıştırılacaktır.
* Python konsolunun `openCodeFile` fonksiyonu ve log dosyasındaki bir satıra karşılık gelen kaynak dosyayı açma komutu için çeşitli küçük düzeltmeler yapıldı.
* NVDA'nın eski sürümlerinde nesne dolaşımı için rol/durum raporlaması yapılırken ortaya çıkan bir sorun düzeltildi.
* Bu eklenti, Edge'de UIA kullanılırken artık ağaç müdahale mekanizmasıyla ilgili bir soruna neden olmuyor.

### Sürüm 2.1

* Tüm kullanım durumlarını ele almak için çeşitli hata düzeltmeleri ve kod yeniden düzenlemesi/temizliği: desteklenen tüm sürümler, kaynak koddan yükleme veya çalıştırma vb. (Łukasz Golonka'nın katkısıyla)
* Compa modülünün yeniden yazılması (Łukasz Golonka'nın katkısıyla)
* Yeniden başlatma iletişim kutusu artık yalnızca bir kez açılabilir.
* Nesne dolaşımı kısayolları artık varsayılan olarak atanmamış durumda ve kullanıcı tarafından eşleştirilmesi gerekiyor.
* Nesne gezgini ile, geçerli nesnenin özelliğini bildirmek için komut dosyasını çağırmak üzere çift tıklama işlemi artık bildirilen bilgileri göz atılabilir bir mesajda görüntülüyor.

### Sürüm 2.0

* Yeni özellik: NVDA'yı yeniden başlatırken bazı ek seçenekleri belirtmek için geliştirilmiş yeniden başlatma iletişim kutusu.
* Yeni özellik: genişletilmiş açıklama modu.
* NVDA'nın 2021.3 öncesi ve sonrası sürümleri arasında hata çalma sesi özelliği uyumlu hale getirildi.
* Yeni özellik: Günlük okuyucu komutları artık günlük görüntüleyicide ve isteğe bağlı olarak düzenleme alanlarında veya web sayfalarında da kullanılabilir.
* Yeni özellik: Python konsolunda, bir nesnenin kaynak kodunu görüntülemek için `openCodeFile` fonksiyonu kullanılabilir.
* Güvenlik nedenleriyle güvenli modda bazı özellikler devre dışı bırakılmıştır.
* Eklentinin uyumluluk aralığı genişletildi (2019.2'den 2021.1'e).
* Sürüm işlemleri artık AppVeyor yerine GitHub Eylemleri ile gerçekleştiriliyor.

### Sürüm 1.0

* İlk sürüm.

[2]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]: https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
