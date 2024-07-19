import bpy
from mathutils import Vector

def create_building(land_area, building_coverage_ratio, floor_area_ratio, height_limit):
    '''
    대지면적: land_area
    건폐율: building_coverage_ratio
    용적률: floor_area_ratio
    높이제한: height_limit
    '''
    # 1층 바닥면적 = 건폐율 * 대지면적
    first_floor_area = building_coverage_ratio * land_area
    
    # 총 층수 = (용적률 * 대지면적) // 1층 바닥면적
    total_floor_area = floor_area_ratio * land_area
    number_of_floors = int(total_floor_area // first_floor_area)
    
    # 각 층 높이 = 높이 제한 / 총 층수
    floor_height = height_limit / number_of_floors
    
    # 장면에 있는 모든 객체 삭제
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 첫 번째 큐브 추가
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, floor_height / 2))
    building = bpy.context.object

    # 바닥 면적의 한 변의 길이 계산
    side_length = first_floor_area ** 0.5

    # 1층 바닥 면적에 맞게 큐브 스케일 조정
    building.scale = (side_length, side_length, floor_height)

    # 층을 복제하고 쌓기
    for i in range(1, number_of_floors):
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'},
                                      TRANSFORM_OT_translate={"value": (0, 0, floor_height)})
    
    # 모든 층 객체를 하나로 결합
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = building
    bpy.ops.object.join()
    
    # 결과 메쉬를 파일로 저장
    file_path = f"result/{first_floor_area}_{number_of_floors}_{floor_height}.obj"
    bpy.ops.wm.obj_export(filepath=file_path)
    print(f"Building created and saved as '{file_path}'")

    # 생성된 건물의 바닥면적 확인
    world_verts = [building.matrix_world @ Vector(v.co) for v in building.data.vertices]
    min_x = min(v.x for v in world_verts)
    max_x = max(v.x for v in world_verts)
    min_y = min(v.y for v in world_verts)
    max_y = max(v.y for v in world_verts)
    length_x = max_x - min_x
    length_y = max_y - min_y
    print(f"Floor area: {length_x * length_y:.2f} square meters")

    # 생성된 건물의 높이 확인
    min_z = min(v.z for v in world_verts)
    max_z = max(v.z for v in world_verts)
    building_height = max_z - min_z
    print(f"Building height: {building_height:.2f} meters")

# 예시 사용법:
create_building(
    land_area=1000,                 # 예시 대지면적 (제곱미터)
    building_coverage_ratio=0.5,    # 예시 건폐율 (50%) → 1층 바닥면적 = 500
    floor_area_ratio=2,             # 예시 용적률 (200%) → 총 층수 = 4
    height_limit=50                 # 예시 높이 제한 (미터) → 각 층 높이 = 12.5
)