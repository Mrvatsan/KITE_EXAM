/**
 * Test script to verify hall seating block and floor logic
 * This tests the logic without running the full application
 */

// Helper function to determine block from hall number
const getBlockFromHallNo = (hallNo: string): string => {
    const hallNum = parseInt(hallNo);
    if (isNaN(hallNum)) return 'Unknown';

    // 3-digit numbers (100-999) = Academic Block
    // 4+ digit numbers (1000+) = Innovation Block
    if (hallNum >= 100 && hallNum <= 999) {
        return 'Academic Block';
    } else if (hallNum >= 1000) {
        return 'Innovation Block (IT Tower)';
    }

    return 'Unknown';
};

// Helper function to determine floor from hall number based on block
const getFloorFromHallNo = (hallNo: string, block: string): string => {
    const hallNum = parseInt(hallNo);
    if (isNaN(hallNum)) return 'Unknown';

    if (block === 'Academic Block') {
        // Use hundreds series for Academic Block
        if (hallNum >= 100 && hallNum <= 199) return 'Ground Floor';
        if (hallNum >= 200 && hallNum <= 299) return 'First Floor';
        if (hallNum >= 300 && hallNum <= 399) return 'Second Floor';
        if (hallNum >= 400 && hallNum <= 499) return 'Third Floor';
        if (hallNum >= 500 && hallNum <= 599) return 'Fourth Floor';
        if (hallNum >= 600 && hallNum <= 699) return 'Fifth Floor';
    } else if (block === 'Innovation Block (IT Tower)') {
        // Use first digit(s) for Innovation Block
        if (hallNum >= 3000 && hallNum <= 3999) return 'Third Floor';
        if (hallNum >= 4000 && hallNum <= 4999) return 'Fourth Floor';
        if (hallNum >= 5000 && hallNum <= 5999) return 'Fifth Floor';
    }

    return 'Unknown';
};

// Test cases
const testCases = [
    // Academic Block tests
    { hallNo: '104', expectedBlock: 'Academic Block', expectedFloor: 'Ground Floor' },
    { hallNo: '204', expectedBlock: 'Academic Block', expectedFloor: 'First Floor' },
    { hallNo: '313', expectedBlock: 'Academic Block', expectedFloor: 'Second Floor' },
    { hallNo: '512', expectedBlock: 'Academic Block', expectedFloor: 'Fourth Floor' },

    // Innovation Block tests
    { hallNo: '3001', expectedBlock: 'Innovation Block (IT Tower)', expectedFloor: 'Third Floor' },
    { hallNo: '4001', expectedBlock: 'Innovation Block (IT Tower)', expectedFloor: 'Fourth Floor' },
    { hallNo: '1003', expectedBlock: 'Innovation Block (IT Tower)', expectedFloor: 'Unknown' }, // Edge case: 1000s series not defined

    // Additional edge cases
    { hallNo: '199', expectedBlock: 'Academic Block', expectedFloor: 'Ground Floor' },
    { hallNo: '200', expectedBlock: 'Academic Block', expectedFloor: 'First Floor' },
    { hallNo: '599', expectedBlock: 'Academic Block', expectedFloor: 'Fourth Floor' },
    { hallNo: '3999', expectedBlock: 'Innovation Block (IT Tower)', expectedFloor: 'Third Floor' },
    { hallNo: '5001', expectedBlock: 'Innovation Block (IT Tower)', expectedFloor: 'Fifth Floor' },
];

console.log('🧪 Testing Hall Seating Block & Floor Logic\n');
console.log('='.repeat(80));

let passCount = 0;
let failCount = 0;

testCases.forEach((test, index) => {
    const block = getBlockFromHallNo(test.hallNo);
    const floor = getFloorFromHallNo(test.hallNo, block);

    const blockMatch = block === test.expectedBlock;
    const floorMatch = floor === test.expectedFloor;
    const passed = blockMatch && floorMatch;

    if (passed) {
        passCount++;
        console.log(`✅ Test ${index + 1}: Hall ${test.hallNo}`);
    } else {
        failCount++;
        console.log(`❌ Test ${index + 1}: Hall ${test.hallNo}`);
        if (!blockMatch) {
            console.log(`   Block: Expected "${test.expectedBlock}", Got "${block}"`);
        }
        if (!floorMatch) {
            console.log(`   Floor: Expected "${test.expectedFloor}", Got "${floor}"`);
        }
    }
    console.log(`   Hall No: ${test.hallNo}`);
    console.log(`   Block: ${block}`);
    console.log(`   Floor: ${floor}`);
    console.log('-'.repeat(80));
});

console.log('\n📊 Test Results:');
console.log(`   Total Tests: ${testCases.length}`);
console.log(`   ✅ Passed: ${passCount}`);
console.log(`   ❌ Failed: ${failCount}`);
console.log('='.repeat(80));

if (failCount === 0) {
    console.log('\n🎉 All tests passed! Logic is working correctly.');
} else {
    console.log('\n⚠️  Some tests failed. Please review the logic.');
}
