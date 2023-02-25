'''Rewrite - JWOOTTS'''

'''Vac shits'''
antivax1 = "kldnaklwndlkawndklnwaklndhu8agwbfawfmsla,dl;am,wd"
antivax2 = "52321" '''Date'''

'''imports'''
import pymem
import requests
import pymem.process
import keyboard
import time
from math import sqrt, pi, atan

'''read offsets from github repo --change offsets on fly'''
offsets_link = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'
response = requests.get(offsets_link).json()

'''signatures'''
dwForceJump = int(response["signatures"]["dwForceJump"])
dwLocalPlayer = int(response["signatures"]["dwLocalPlayer"])
dwEntityList = int(response["signatures"]["dwEntityList"])
dwForceAttack = int(response["signatures"]["dwForceAttack"])
dwGlowObjectManager = int(response["signatures"]["dwGlowObjectManager"])
dwClientState = int(response["signatures"]["dwClientState"])
dwClientState_ViewAngles = int(response["signatures"]["dwClientState_ViewAngles"])
m_bDormant = int(response["signatures"]["m_bDormant"])

'''netvars'''
m_fFlags = int(response["netvars"]["m_fFlags"])
m_crossHairID = int(response["netvars"]["m_iCrosshairId"])
iTeamNum = int(response["netvars"]["m_iTeamNum"])
m_iObserverMode = int(response["netvars"]["m_iObserverMode"])
m_flFlashMaxAlpha = int(response["netvars"]["m_flFlashMaxAlpha"])
m_bSpotted = int(response["netvars"]["m_bSpotted"])
m_clrRender = int(response["netvars"]["m_clrRender"])
m_iGlowIndex = int(response["netvars"]["m_iGlowIndex"])
m_iHealth = int(response["netvars"]["m_iHealth"])
m_dwBoneMatrix = int(response["netvars"]["m_dwBoneMatrix"])
m_vecOrigin = int(response["netvars"]["m_vecOrigin"])
m_vecViewOffset = int(response["netvars"]["m_vecViewOffset"])

'''client vars'''
pm = pymem.Pymem("csgo.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

'''inital vals'''
aimfov = 120

'''user def functions'''
def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY > -180:
        viewAngleY += 360

    return viewAngleX, viewAngleY

def checkAngles(x, y):
    if x > 89:
        return False
    elif x <-89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True

def nanChecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True

def calcDistance(cur_x, cur_y, new_x, new_y):
    distanceX = new_x - cur_x
    if distanceX < -89:
        distanceX += 360
    elif distanceX > 89:
        distanceX -= 360
    if distanceX < 0.0:
        distanceX = -distanceX

    distanceY = new_y - cur_y

    if distanceY < -180:
        distanceY += 360
    elif distanceY > 180:
        distanceY -= 360
    if distanceY < 0.0:
        distanceY = -distanceX

    return distanceX, distanceY

def calcAngle(localPos1, localPos2, localPos3, enemyPos1, enemyPos2, enemyPos3):
    try:
        delta_x = localPos1 - enemyPos1
        delta_y = localPos2 - enemyPos2
        delta_z = localPos3 - enemyPos3
        hyp = sqrt(delta_x * delta_x + delta_y * delta_y + delta_z * delta_z)
        x = atan(delta_z / hyp) * 180 / pi
        y = atan(delta_y / delta_x) * 180 / pi
        if delta_x >= 0.0:
            y += 180.0
        return x, y
    except:
        pass


def main():

    '''Grab user properties'''
    print("")
    print("Welcome to Project-Marco")
    print("------------------------")
    print("")
    get_enableBHops = input("Enable Hops? y/n: ")
    get_enableThirdPerson = input("Enable 3rd Person? y/n: ")
    get_enableNoFlash = input("Enable No-Flash? y/n: ")
    get_enableBackTrack = input("Enable BackTrack? y/n: ")
    get_enableRadar = input("Enable Radar? y/n: ")
    get_xRay = input("Enable X-Ray? y/n: ")
    get_aimBot = input("Enable Aimware? y/n: ")

    if get_enableBHops == "y" or get_enableBHops == "Y":
        ENABLE_BHOPS = True
        print(ENABLE_BHOPS)
    else:
        ENABLE_BHOPS = False
    if get_enableThirdPerson == "y" or get_enableThirdPerson == "Y":
        ENABLE_THRIDPERSON = True
    else:
        ENABLE_THRIDPERSON = False
    if get_enableNoFlash == "y" or get_enableNoFlash == "Y":
        ENABLE_NOFLASH = True
    else:
        ENABLE_NOFLASH = False
    if get_enableBackTrack == "y" or get_enableBackTrack == "Y":
        ENABLE_BACKTRACK = True
    else:
        ENABLE_BACKTRACK = False
    if get_enableRadar == "y" or get_enableRadar == "Y":
        ENABLE_RADARCHAMS = True
    else:
        ENABLE_RADARCHAMS = False
    if get_xRay == "y" or get_xRay == "Y":
        ENABLE_XRAY = True
    else:
        ENABLE_XRAY = False
    if get_aimBot == "y" or get_aimBot == "Y":
            ENABLE_AIMWARE = True
    else:
        ENABLE_AIMWARE = False

    print("Config Set. Press end to edit - end config.")

    switch = 0

    while True:
        try:
            '''Set local player vars'''
            localPlayer = pm.read_int(client + dwLocalPlayer)
            engine_pointer = pm.read_int(engine + dwClientState)
            crossHairID = pm.read_int(localPlayer + m_crossHairID)
            getTeam = pm.read_int(client + dwEntityList + ( crossHairID - 1) * 0x10)
            localTeam = pm.read_int(localPlayer + iTeamNum)
            crosshairTeam = pm.read_int(getTeam + iTeamNum)

            target = None
            oldDistX = 11111111111
            oldDistY = 11111111111


            if keyboard.is_pressed("end"):
                print("")
                userInput = input ("Type X to edit config... Or W to Exit program.")
                if userInput == "X" or userInput == "x":
                    print("")
                    print("~-~-Editing Config-~-~")
                    print("----------------------")
                    get_enableBHops = input("Enable Hops? y/n: ")
                    get_enableThirdPerson = input("Enable 3rd Person? y/n: ")
                    get_enableNoFlash = input("Enable No-Flash? y/n: ")
                    get_enableBackTrack = input("Enable BackTrack? y/n: ")
                    get_enableRadar = input("Enable Radar? y/n: ")
                    get_xRay = input("Enable X-Ray? y/n: ")
                    get_aimBot = input("Enable Aimware? y/n: ")

                    if get_enableBHops == "y" or get_enableBHops == "Y":
                        ENABLE_BHOPS = True
                    else:
                        ENABLE_BHOPS = False
                    if get_enableThirdPerson == "y" or get_enableThirdPerson == "Y":
                        ENABLE_THRIDPERSON = True
                    else:
                        ENABLE_THRIDPERSON = False
                    if get_enableNoFlash == "y" or get_enableNoFlash == "Y":
                        ENABLE_NOFLASH = True
                    else:
                        ENABLE_NOFLASH = False
                    if get_enableBackTrack == "y" or get_enableBackTrack == "Y":
                        ENABLE_BACKTRACK = True
                    else:
                        ENABLE_BACKTRACK = False
                    if get_enableRadar == "y" or get_enableRadar == "Y":
                        ENABLE_RADARCHAMS = True
                    else:
                        ENABLE_RADARCHAMS = False
                    if get_xRay == "y" or get_xRay == "Y":
                        ENABLE_XRAY = True
                    else:
                        ENABLE_XRAY = False
                    if get_aimBot == "y" or get_aimBot == "Y":
                        ENABLE_AIMWARE = True
                    else:
                        ENABLE_AIMWARE = False

                    print("Done Editing Config please return to game....")

                elif userInput == "W" or userInput == "w":
                    exit(0)
                else:
                    print("Invalid input. Please press end to retry in game.")

            '''b-hops'''
            if ENABLE_BHOPS:
                if keyboard.is_pressed("space"):
                    force_jump = client + dwForceJump
                    player = pm.read_int(client + dwLocalPlayer)
                    onGround = pm.read_int(player + m_fFlags)
                    if player and onGround and onGround == 257:
                        pm.write_int(force_jump, 5)
                        time.sleep(0.06)
                        pm.write_int(force_jump, 4)

            '''3rd person'''
            if ENABLE_THRIDPERSON:
                if keyboard.is_pressed("z") and switch == 0:
                    pm.write_int(localPlayer + m_iObserverMode, 1)
                    switch = 1
                    time.sleep(0.05)
                elif keyboard.is_pressed("z") and switch == 1:
                    pm.write_int(localPlayer + m_iObserverMode, 0)
                    switch = 0
                    time.sleep(0.05)

            '''backtrack'''
            if ENABLE_BACKTRACK:
                if crossHairID > 0 and crossHairID < 52 and localTeam != crosshairTeam:
                    pm.write_int(client + dwForceAttack, 6)

            '''no flash'''
            if ENABLE_NOFLASH:
                if(localPlayer):
                    flash_val = (localPlayer + m_flFlashMaxAlpha)
                    if flash_val:
                        pm.write_int(flash_val, 0)


            '''radar - chams'''
            rgbT = [255,51,0]
            rgbCT = [0,51,255]

            if ENABLE_RADARCHAMS:
                for i in range(1,32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        pm.write_int(entity + m_bSpotted, 1)
                        entity_team_id = pm.read_int(entity + iTeamNum)

                        if entity_team_id == 2:
                            pm.write_int(entity + m_clrRender, 255)
                            pm.write_int(entity + m_clrRender + 0x1, 51)
                            pm.write_int(entity + m_clrRender + 0x2, 0)

                        elif entity_team_id == 3:
                            pm.write_int(entity + m_clrRender, 0)
                            pm.write_int(entity + m_clrRender + 0x1, 51)
                            pm.write_int(entity + m_clrRender + 0x2, 255)
                        else:
                            pass


            '''X-Ray'''
            if ENABLE_XRAY:
                glow_manager = pm.read_int(client + dwGlowObjectManager)
                for i in range(1,32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        entity_glow = pm.read_int(entity + m_iGlowIndex)
                        entity_team_id = pm.read_int(entity + iTeamNum)

                        if entity_team_id == 2:
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1.0))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0.0))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0.0))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1.0))
                            pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)

                        elif entity_team_id == 3:
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0.0))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0.0))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1.0))
                            pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1.0))
                            pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)


            '''aimware'''
            if ENABLE_AIMWARE:
                for i in range(1, 32):
                    entity = pm.read_int(client + dwEntityList + i * 0x10)
                    if entity:
                        try:
                            entity_team_id = pm.read_int(entity + iTeamNum)
                            entity_hp = pm.read_int(entity + m_iHealth)
                            entity_dormant = pm.read_int(entity + m_bDormant)
                        except:
                            print("find player info once")


                        if localTeam != entity_team_id and entity_hp > 0:
                            entityBones = pm.read_int(entity + m_dwBoneMatrix)
                            localposx_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles)
                            localposy_angles = pm.read_float(engine_pointer + dwClientState_ViewAngles + 0x4)
                            localposz_angles = pm.read_float(localPlayer + m_vecViewOffset + 0x8)
                            localPos1 = pm.read_float(localPlayer + m_vecOrigin)
                            localPos2 = pm.read_float(localPlayer + m_vecOrigin + 4)
                            localPos3 = pm.read_float(localPlayer + m_vecOrigin + 8) + localposz_angles

                            try:
                                entitypos_x = pm.read_float(entityBones + 0x30 * 8 + 0xC)
                                entitypos_y = pm.read_float(entityBones + 0x30 * 8 + 0x1C)
                                entitypos_z = pm.read_float(entityBones + 0x30 * 8 + 0x2C)

                            except:
                                continue

                            X, Y = calcAngle(localPos1, localPos2, localPos3, entitypos_x, entitypos_y, entitypos_z)
                            newDist_x, newDist_y = calcDistance(localposx_angles, localposy_angles, X, Y)



                            if newDist_x < oldDistX and newDist_y < oldDistY and newDist_x <= aimfov and newDist_x <= aimfov:
                                oldDistX, oldDistY = newDist_x, newDist_y
                                target, target_hp, target_dormant = entity, entity_hp, entity_dormant
                                target_x, target_y, target_z = entitypos_x, entitypos_y, entitypos_z



                        if keyboard.is_pressed("alt") and localPlayer:
                            if target and target_hp > 0 and not target_dormant:
                                x,y = calcAngle(localPos1, localPos2, localPos3, target_x, target_y, target_z)
                                normalizex, normalizey = normalizeAngles(x,y)

                                pm.write_float(engine_pointer + dwClientState_ViewAngles, normalizex)
                                pm.write_float(engine_pointer + dwClientState_ViewAngles + 0x4, normalizey)
        except:
            print("round has not began.")



if __name__ == '__main__':
    main();
