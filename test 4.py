from core.crud.sql.artist import get_all_by_ids

import io
from PIL import Image
import requests
import time


class Image_size:
    micro = 80
    tiny = 160
    small = 320
    medium = 640
    large = 800
    extra = 1280


def get_artist_image_url(artist_uuids: list):
    db_artists = get_all_by_ids(artist_uuids)
    for db_artist in db_artists:
        ext = db_artist.ext['resize_images']
        with open("query_result_image_size.txt", "a") as f:
            for resize_images in ext:
                type = resize_images.split(".")[-2]
                image_url = f"https://s3.amazonaws.com/{resize_images}"
                original_image_url = f"https://s3.amazonaws.com/{db_artist.ext['square_image']['uri']}"
                if type == 'micro':
                    checking = test_2(image_url) == Image_size.micro
                elif type == 'tiny':
                    checking = test_2(image_url) == Image_size.tiny
                elif type == 'small':
                    checking = test_2(image_url) == Image_size.small
                elif type == 'medium':
                    checking = test_2(image_url) == Image_size.medium
                elif type == 'large':
                    checking = test_2(image_url) == Image_size.large
                elif type == 'extra':
                    checking = test_2(image_url) == Image_size.extra
                else:
                    print("Error")
                result = f"type: {type}, artist_uuid: {db_artist.uuid}, original_image_url: {original_image_url}, image_url: {image_url}, size: {test_2(image_url)}, result: {checking}"
                print(result)
                f.write(result + "\n")
def test_2(uri):
    response = requests.get(uri)
    image_bytes = io.BytesIO(response.content)
    img = Image.open(image_bytes)
    return img.size[0]


if __name__ == "__main__":
    start_time = time.time()
    # uri = "https://s3.amazonaws.com/vibbidi-images/artists/img_D1F90D01CB164FD5B970D06EB0E7033B.2020.06.11.15.21.13.small.jpg"
    # test_2(uri)
    artist_uuids = [
        "71BBDC06F6F34983853B3EAF5491EACA",
        "D96658C02F8C4293A16AE37CE2CBC387",
        "1422E730478D4EFFB637B0319A50F2FD",
        "7ED02D0C64CA4E13885370D005B4CA14",
        "18DD1A64395C4428B7E1CF9F620A7B55",
        "E7F5AD12A97B418DA07B48326C894618",
        "E6D1BC87FA2E4D2898BDAD55741D3C95",
        "BDB4D58BF29F4E55AFBD3C7E5695FB6E",
        "8B7407B3841F48519BFC7D87E7450BCA",
        "F4F8B6D1B32B4B93A94D5B64AF755B21",
        "062D886C979A454C9FAB5CBE08E8164D",
        "065F0D3E2F1848089197C3C1457F1036",
        "0B2EE820671C450399DE4B2C428A6B2C",
        "35D9A8D5AA9F4A38B34B5A9EC537CA3D",
        "8A39D6EA93E6408AA9625EC21E187A31",
        "ED0FFF068E9D04616873AB568F3A6BE7",
        "8CFDF00909394812B0955DFFBA5289A0",
        "BDD9F256822742579EA3B3BDFC40D20D",
        "65565DB0A46E46759E641D18A42BDD92",
        "62773AF7FF6C46FF9DA64C3B7EE295BC",
        "53138C83C55B4E0591C8353EBA2202F7",
        "EDE1B9EBD7F540CFAF980A0CAA59359B",
        "BAA9626EBC2C40F0B7B9859567667440",
        "5B7F9DCB0279448BAB1B32FDF7853CA8",
        "4053B91BDC92452E82BA238B1C012163",
        "31CA561B19294562957E7B7A1DED2330",
        "AB0EB53C89034228929C8D5C27C51EC3",
        "D7BDFFAA771C4ABE9756548F417849AB",
        "E07E8AC7146A41E38A28C5BD9F78CC1E",
        "EB0B02464A3840CE9BFF6C493EC8F50B",
        "95A70B37771B4CEA822931E494234F07",
        "28CB3DEBBB39430A9754EE5F763183DA",
        "C78C9C09B58C4566948CB7A0757E2495",
        "4A8678B97C0B4C908A4D0210962EE8B9",
        "6B4B3F8BFBD44997B1FF2C87EB271231",
        "88D4BB4A0DF74CEC950413F739ECE5B7",
        "BE3C801B45D64F438ABADCDA7EC6E350",
        "ED9A34583CE84096B30D93812AD11B91",
        "5EC82DF5C9744B1FAA2865699EB0E938",
        "D116B189046C46AC92130180FA3DDEB4",
        "67E5B275449B4EF49CF13FA770767357",
        "7B4021B036B24E22A3F3AC6CBA059CD9",
        "0EC29516BD2843C6BCD1F2888533C267",
        "5DBB5F24C2824D7E9C1DAF212422A745",
        "DCC72869CC4C647E0B26AD4DB8EC0540",
        "F622C9F20F564AD9A855EED67C31A071",
        "6679C9D1BDAE45D6AA7456F379B65BB5",
        "CE24FEDE8FEA4303BAC2D2F96F21B2B8",
        "0C7A70D20EAD4D8C83CCF6EBA6925C1C",
        "EF1F0CE1730646F981C1187F216A5D92",
        "BA7B22CE7E91477194D7106DD66EFEE1",
        "A6CD35CB188C455ABBD3D95DF52F3DD9",
        "C335E69C37714D81BC4F616240951EC6",
        "409082F7CD224EFEA36978CAF4885C50",
        "94BDBA88E6744861913F50ADE0026E07",
        "FC7C6E3D31BD4BC1AA12ADF7D09E0933",
        "57E4F93ED6914533AA8A451AD5CD5DB9",
        "63E53059C60D4997BB454D3B2FFF084C",
        "CFC3B2A70DFB471ABD662DF1BBC320FF",
        "568F1D478EB4466FBB5171B38C6268D3",
        "FA061D2D31419473ABF5E84168E8784E",
        "62F59AD3DD44425B84F281DEF1883211",
        "EB353DB872F84F87A12985B0438AC0A1",
        "16027125F3B446578B576F18505C4484",
        "71C62E2591684F03AB424C9ACAC81020",
        "91C6BB51F34341D4ACE08E5DEE08FB13",
        "A24E0F1564814C7BA0B9C945C0DB6876",
        "8F0AA6CC94DE42658AA7F3F3052B3DF9",
        "00B2DE8F56BA4C94A3B315F36992CE02",
        "8EBD9C44611C42E8AC0910C13073BFFB",
        "903CAE23B5FB4E1E9D8A83806F91A353",
        "A6B360E3F05541C7B52A8F04FA133558",
        "0DB587387AFC4F3393E4D143A560C715",
        "84F0A655B0D945F8A056814273BFBEF3",
        "7D03D917C66F4586A91854E5552CAB30",
        "63A7D9F716E14E52A41EE47E31D94BBE",
        "2F92459ECD5F49DC994E3207920243F9",
        "7F4C8F614F0349CFB276DCEC63965B28",
        "D81C66E77A304A87B43D2E3E78A4D07C",
        "920998BD45964230952D91B907DC721E",
        "CD349DACACC24793B87986C59B957599",
        "72791FDD47E4462FA8B807DF4FAF76CE",
        "08F45671955C464DA8C5E77AC551242A",
        "1747957DA5A0430585257BA8796BEC20",
        "5D81351CF1074F63ADC015D69A14C0E5",
        "E27FD7D18F99427CBB2C468AB1E7A5E5",
        "072B383103734F3F913268AB0100CB00",
        "720726CF6BF7449D9714A76701220F74",
        "247849E6041A4478B1C236CD05B57822",
        "6D703C02E3BB4087822EBEA30E010A18",
        "D3D19A5AA8EC34B95B4469C1CE41FAF1",
        "81A502C988FA4BFE9C47A48D9BD41D7C",
        "099658429C8D4DB89C1705FA483C5741",
        "211B2D057DC64D3FB31FEDD22BC91179",
        "E8C4273A09D740D5A105BB868C1989EC",
        "D563D7CDB6D74DEAAE9A0ACD117C3707",
        "9F28317D56809428AB2DE4265584DAD0",
        "CB7BCC0799B14697B8BD9C6440E16F38",
        "2114EF5C4998418FA298A1DF4C98995A",
        "50E1C16CD47E427EB9D0E231ED7DFCE0",
        "995D8D8BF79F40A48E1D2D7DFC916665",
        "D63AE80B058A484FBF4A6390E1333B53",
        "FBA30A9E422E4E918B812B0A10ACD23C",
        "C6AE6244974944EA8A59CDA23E54CEBA",
        "82520C19B582486BBFE66744E3CE3D3D",
        "432D1FACD4D54C759E21C9296F4FD10E",
        "9AD6D39E51934BD6A8F71D069C66B6EC",
        "4E68A71C5856417C9906C45BCCC6B2D1",
        "FB6F4A23806149299AEBA37DB050871C",
        "814B350485324C84ACE2FAEF571CC2BA",
        "49BF36C034814EFAA0D762494DE85EB0",
        "5D7B0176EEDA4FB68B12A5E470E642D3",
        "C1CA4C29376F4C6F80F230B14D27EFB2",
        "F24555EAD6C1476DA066300D6BFB8BC2",
        "7748893B48514C259DD4CDE22C7C74C5",
        "059854AC9694450992B1F2E4FAB90CF5",
        "AA20EC8EA0684EC4B3845C5FECA08A0A",
        "F0AB93B410854F48A450977BC3DB0CD6",
        "C698B8A3476A48AC86F53B29518EE64A",
        "C7FEAAEAFE9747A584D1F839DD5A6A16",
        "BDEAF959A50440AC9A9C4D079219F369",
        "4CB09445FF4C4D06A3373FB04088839B",
        "8F44978E47FC44899A1FA1424E56A3EB",
        "A62F64FA06584B86A087F0CAA0EC523F",
        "147787D769D14D5299DB799222663F49",
        "918AA42F804F436C8683950068154968",
        "9273CAAF3E1348809F82D6537568C80D",
        "CC3E08B4C6C54E17B973C7C0927184F9",
        "BC79215071224A9F8AE8D1BBC5456529",
        "090CFCAC1AE4645A3BA5ADF568E5DE86",
        "13C95D28966E4A0CAB5FD8AF7824CEA4",
        "416436AE4D394818BB88DE166EC48F91",
        "B9FC9D1CE3974B56A49C9AA35A68F421",
        "E96C6DC168804C4B9A7FC13D8CB27BC4",
        "1B64F90C8B134EEA97CACC395BEA66E5",
        "3CA58A42FD5D4DF18829540EAC2E60BE",
        "F4A7550BCB43410DBE2BF92D7C1D8108",
        "F3D57D86981F44B682288009B7D016F9",
        "34853495695C4CB2951A7110F93B8AFA",
        "B524D0E8F51C407EB2C456D5D2D519AD",
        "B1C4ABB1452C45F9A22856CAE26D67C7",
        "60E12B9BB7634733BB5412233483D028",
        "26597D38FF0D415B9602839C94E75DAE",
        "C3005F49936D474FBE87C346161924A9",
        "7E901F9F226A4C768DBF4D351ACC9E5C",
        "A8D7FC8FF44B42078A62CFC9320F8AED",
        "55575B35C80640928114D683D87DB6EC",
        "2FA8C18C38CB4422B0D9D74E8A2C2CEF",
        "BE058A45794A4D8D833FBFA452575CC8",
        "B95B3408D81644F082CA9C588576C649",
        "63761733499D4C84B2A72A79F784562C",
        "A106CB0213FA4E839D8D02D9D251130D",
        "9F586F084D244A208EA5349A1F98002A",
        "1D017B4411534721912EE4D0441BA614",
        "9C39614111994D8DBC58343CD0617535",
        "DA76D0F08551462A865027C336DE9B0E",
        "89A1A5689E29489DA2282693E6620C36",
        "04FA89349F19470A8A977FE3A222AB03",
        "92211AC1CF6148A2AF73BCA441150F7B",
        "A5C7DC075ACE4202A2E831F3E955F8D3",
        "71AA3672BB3D4882900C04DDE6987266",
        "72F5B05618D1455692366B10CCE1BF37",
        "E5C7145DB4764A7088E8493D50CDB849",
        "8DBD1060A8A64375B4D01A2188B15D14",
        "2136D07CAECF42E7A2FFF896CE821ECC",
        "8ADF9C9C6E7241AEA294526750AE9C30",
        "5116A6C84EA64FBC9CFE94E9FC9D3058",
        "5EDBA91030C44B15B9A2F8A048DA8262",
        "479A81F3B2F243AD97CDF8E5C3A6E78D",
        "28471D981B214663A35C2EDF98F7703A",
        "76B971F8D5AB47F2B469D674AF45E8FE",
        "809146CFE05A49BC86248D5621A20025",
        "28AD1CDF16544879805719063A22D799",
        "FA646EF33B934A95B00EDD059E6580EA",
        "FD249BBA13364527A6368CDD86B4FAEC",
        "FDC4DC8155374A94BF041490672BC629",
        "ACAE2685BA8E42B9B4223139C6734C96",
        "357C4DE6E50943399C2C8F7E1E5DE955",
        "2C4FF11F30B546038A0620280EA9E8D7",
        "AE65443849E641F7826AA4D95A8ED638",
        "7DB2EE2C2DCB400A83BE1A6EFAC6969A",
        "B7170432EFB344A4B54AA1EB5A81DEC1",
        "F70E6FC1499B42EA977E20C4C70180BD",
        "D93B1C6B026442FA8ACAB6B58A608FC3",
        "9DB6020330EE4EEEBF41EE9C1648A390",
        "72CB380CBFDC421A9A901729343BBFA9",
        "22F4A4C39CB7D488DB26AC49448628E2",
        "3EBB68524D6D48FD9CED4A2B8A90D650",
        "3346AAB4BBB54DA490ADAA6E2109A5E2",
        "90D0E7D6D4BD4C9A9AF57032B2C12D31",
        "9F8EE3B393D94B6D84D238235D222943",
        "F2EF3613358F45E3816369916F2BEF26",
        "B682B4C6645B4153A492D775083CA2C8",
        "FB9D299ADD2B40A089F1D50B91B6596E",
        "02836A750CC04DA797EA0061DBA44916",
        "83A2DAADBA7D47F48879146B369ED3D5",
        "B4CCBF089CC54CB088ECD2C14779ED17",
        "4CA50E46616D4C4D9C8FBC53895A79CB",
        "4C1A33EE1F584437A26700EDA69B3E42",
        "3407269F250742989CFE4547EB4DC8B1",
        "62AF0DEE1D984C66A2EE6A2FBA24642C",
        "6E149FA09139C4EE5B1813E40E91FB06",
        "C345C3CB892742659041626250756B23",
        "D68D9398E17FD4B95AD49B8DD0F37390",
        "69FB2780878F49AFA7C52F4E55D81F4E",
        "DB4709289BF24F5596CAF045DD8582CA",
        "F943B5DCA1834949B03C05FC39610CF5",
        "E89949FCB81C4C9388D0BA9D7CC03FE6",
        "16F7A9740A614EE6807A3788F68329FF",
        "92B771217D82493DA8EE202A284968F2",
        "F1D6E2A1C142F4FD1B5C93E306390550",
        "2F4D8DCC371942A584DC6A176D2BE390",
        "EE2B870FD8CC40378CC9A6D3B7B8A220",
        "1F871C0B2DA04ADE968390034730B3E6",
        "2FF796DC62694470AB6427799E24A04A",
        "B1B6F981CA63494EA1790770C605C7CC",
        "35D5C2822B0D43D8AD828FBC4D87D46E",
        "736B87CD4CC1471CBB1EE85FA39C78ED",
        "AA41135A6D64147EEAD1F59B45AE35CE",
        "6D4DA234E31D4467B1C488F80381769A",
        "32BDCD1169234AC6B9F0A67A04FB2579",
        "16640CBFFC8D44F18411C88BF50D6FA6",
        "2725CE31918A4F9E9B7A6D226D0BD9D0",
        "934071EE7FE648179C4C29B750DF173A",
        "40E399333B574401AA665D191F7B861B",
        "3B586EDD784B4C42AFBF0CE1D7840EF3",
        "29107D56F7814E54BAFB5D86ED1988EE",
        "E363398B758A4BB6957D9F15BACDC8C4",
        "9A109E45492A4B0C90039301038B58B1",
        "66421BA657794F8FB682626CE5B25539",
        "1F7BACFA0273456CBC46054F13335014",
        "CC0D0ABBD17D4BFFBE1DF7435FDDF986",
        "797BA88CDE4B48399B835DD83A550A21",
        "4D55F85B159B94E5A9927252B22B7156",
        "6BB46235A7EE4F76B451210BAD69FFF0",
        "D6B0A17CA35A43548C4E4C52938DFCCA",
        "638C752B1F3546A6B8D33C87D1035F7F",
        "B11D30A3DFD847BDBB64CD526314876D",
        "B89082FA65314DBEB203710A059DC8F4",
        "5017EBE6AB3F4F8FA6F0948AE4F5BB2E",
        "DB766B3E85D246948DD35B6237740321",
        "758EB6EA11C4945098996712EE98E6AB",
        "563A16836DDD477C9C94E1CC1F66F797",
        "1DA4F01957964A329FBBE5A475729A4E",
        "8CF47CF6C9F44899AE967AE40897BA46",
        "D1F90D01CB164FD5B970D06EB0E7033B",
        "0F478F399E4B473FBB5069CE3624D149",
        "623121C3823B47A6A2AE25DF36A99FAF",
        "90F0B066BF2E4105B5D9AAB8180D7817",
        "76DC990F98B849999FE7306F280136B9",
        "DAD118B5EB134126B9374D47C129DDFA",
        "CFC0D52DBAA14D89926125A08C394C43",
        "225AAA5FECD14AE3A9D9A0F85E66F517",
        "18D915EA23064907B3056D64B9E05939",
        "9421E6C0C55E470EB69F269B70E8C0BC",
        "224327CBA4B1C48249B4532F4FEB04DF",
        "09251D0F75DA4F0DB0C5F6186CEC3E54",
        "8E298EBD1F364F50952AEFD75194C85D",
        "8D0B42BCA68C4CBB87FF788C671799CF",
        "CF4F47F7F9E7425186B109A1426F2F48",
        "3B330E4195AE4448AD5AC1A20723DEC9",
        "A9C67AA767F44890B73B97CFBF31F487",
        "67AFFF77C649463BBC29E1091256B88D",
        "BCF9336CCA2F4C7CA91858AD5CD1C60E",
        "ED23D5BC65444D73B5DE791F2DD379C0",
        "6ADA85E15CD7448DA3353E922256EFF9",
        "0149FFE3FB9741588F28EA4CA0BA64BE",
        "6EB0E03E152A429BAFB3C913ADE60A48",
        "56F5D1D2143F4C1DA60CEFC4721C6B3E",
        "956ECDEC45544837ABACF0DFE463A355",
        "C6FF250464144AEAA14F85586E7E986F",
        "A3FECBFD0FF746898FD0EBDA6B615559"
    ]
    get_artist_image_url(artist_uuids)

    print("--- %s seconds ---" % (time.time() - start_time))