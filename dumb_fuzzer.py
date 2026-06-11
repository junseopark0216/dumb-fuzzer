# fuzzer.py

import subprocess
import random
import os
import shutil
import time
import signal

# Crash로 인정할 Signal 목록
CRASH_SIGNALS = {
    signal.SIGSEGV,  # Segmentation Fault
    signal.SIGABRT,  # Abort
    signal.SIGBUS,   # Bus Error
    signal.SIGILL,   # Illegal Instruction
    signal.SIGFPE    # Floating Point Exception
}


def Mutator(data, rate):
    """
    Mutation Operators
    - Flip
    - Insert
    - Delete
    - Duplicate
    """

    mutated = bytearray(data)

    if len(mutated) == 0:
        return bytes([random.randint(0, 255)])

    mutation_type = random.choice([
        "flip",
        "insert",
        "delete",
        "duplicate"
    ])

    # -------------------------
    # Byte Flip
    # -------------------------
    if mutation_type == "flip":

        num_flips = max(
            1,
            int(len(mutated) * rate)
        )

        for _ in range(num_flips):

            idx = random.randint(
                0,
                len(mutated) - 1
            )

            mutated[idx] = random.randint(
                0,
                255
            )

    # -------------------------
    # Byte Insert
    # -------------------------
    elif mutation_type == "insert":

        insert_count = max(
            1,
            int(len(mutated) * rate)
        )

        for _ in range(insert_count):

            pos = random.randint(
                0,
                len(mutated)
            )

            mutated.insert(
                pos,
                random.randint(0, 255)
            )

    # -------------------------
    # Byte Delete
    # -------------------------
    elif mutation_type == "delete":

        if len(mutated) > 1:

            delete_count = min(
                max(1, int(len(mutated) * rate)),
                len(mutated) - 1
            )

            for _ in range(delete_count):

                if len(mutated) <= 1:
                    break

                pos = random.randint(
                    0,
                    len(mutated) - 1
                )

                del mutated[pos]

    # -------------------------
    # Byte Duplicate
    # -------------------------
    elif mutation_type == "duplicate":

        if len(mutated) > 0:

            start = random.randint(
                0,
                len(mutated) - 1
            )

            max_len = min(
                16,
                len(mutated) - start
            )

            block_len = random.randint(
                1,
                max_len
            )

            block = mutated[
                start:start + block_len
            ]

            insert_pos = random.randint(
                0,
                len(mutated)
            )

            mutated[
                insert_pos:insert_pos
            ] = block

    return bytes(mutated)


def Fuzzing(
    target_bin,
    seeds,
    use_seed,
    rate,
    crash_dir,
    tmp_dir
):

    count = 0

    while True:

        count += 1

        # 1. 시드 선택
        if use_seed:

            seed_path = random.choice(seeds)

            with open(seed_path, 'rb') as f:
                data = f.read()

        else:

            data = bytes(
                [random.randint(0, 255) for _ in range(32)]
            )

        # 2. 변이 수행
        mutated_data = Mutator(
            data,
            rate
        )

        # 3. 임시 입력 생성
        input_path = os.path.join(
            tmp_dir,
            f"fuzz_{time.time()}"
        )

        with open(input_path, 'wb') as f:
            f.write(mutated_data)

        try:

            # 4. 실행
            proc = subprocess.run(
                [target_bin, "-s", input_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=1
            )

            # 5. Crash 탐지
            if proc.returncode < 0:

                sig_num = -proc.returncode

                try:
                    sig_enum = signal.Signals(
                        sig_num
                    )

                except ValueError:
                    sig_enum = None

                if sig_enum in CRASH_SIGNALS:

                    crash_name = os.path.join(
                        crash_dir,
                        f"bug_{time.time()}.crash"
                    )

                    shutil.copy(
                        input_path,
                        crash_name
                    )

                    print(
                        f"\n[!!!] CRASH DETECTED "
                        f"| Signal={sig_enum.name} "
                        f"| Saved={crash_name}"
                    )

        except subprocess.TimeoutExpired:
            pass

        except Exception as e:

            print(
                f"\n[*] Error: {e}"
            )

        finally:

            try:

                if (
                    input_path
                    and os.path.exists(input_path)
                ):
                    os.remove(input_path)

            except OSError:
                pass

        # 6. 상태 출력
        if count % 50 == 0:

            print(
                f"[*] 실행 횟수: {count}회 진행 중...",
                end='\r'
            )


if __name__ == "__main__":

    target = input(
        "타겟 바이너리 경로: "
    )

    use_seed_input = input(
        "시드 파일을 사용하시겠습니까? (y/n): "
    ).lower()

    seeds = []
    use_seed = False

    if use_seed_input == 'y':

        seed_folder = input(
            "시드 파일 폴더 경로: "
        )

        ext = input(
            "시드 파일 확장자 입력 (전체 선택은 엔터): "
        )

        seeds = [
            os.path.join(seed_folder, f)
            for f in os.listdir(seed_folder)
            if f.endswith(ext)
            and os.path.isfile(
                os.path.join(seed_folder, f)
            )
        ]

        if not seeds:

            print(
                "[!] 오류: 해당 조건의 파일이 없습니다."
            )

            exit()

        use_seed = True

        print(
            f"[*] 시드 파일 {len(seeds)}개 발견"
        )

    else:

        print(
            "[*] 랜덤 데이터 기반 퍼징 모드 활성화"
        )

    choice = int(
        input(
            "변이 강도 선택 "
            "(1: 0.1%, 2: 1%, 3: 5%, 4: 10%, 5: 20%): "
        )
    )

    rates = {
        1: 0.001,
        2: 0.01,
        3: 0.05,
        4: 0.1,
        5: 0.2
    }

    os.makedirs(
        "./crash",
        exist_ok=True
    )

    os.makedirs(
        "./tmp",
        exist_ok=True
    )

    print(
        f"[*] Fuzzing 시작 | 타겟: {target}"
    )

    Fuzzing(
        target,
        seeds,
        use_seed,
        rates.get(choice, 0.01),
        "./crash",
        "./tmp"
    )
